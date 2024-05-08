const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const client = redis.createClient();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const listProducts = [
	{ itemId: 1, itemName: 'Suitcase 250', price: 50, stock: 4 },
	{ itemId: 2, itemName: 'Suitcase 450', price: 100, stock: 10 },
	{ itemId: 3, itemName: 'Suitcase 650', price: 350, stock: 2 },
	{ itemId: 4, itemName: 'Suitcase 1050', price: 550, stock: 5 }
];

const getItemById = (itemId) => {
	return listProducts.find(product => product.itemId === itemId);
};

const reserveStockById = async (itemId, quantity) => {
	await setAsync(`item.${itemId}`, quantity);
};

const getCurrentReservedStockById = async (itemId) => {
	const reservedStock = await getAsync(`item.${itemId}`);
	return reservedStock ? parseInt(reservedStock) : 0;
};

app.get('/list_products', (req, res) => {
	const formattedProducts = listProducts.map(product => ({
		itemId: product.itemId,
		itemName: product.itemName,
		price: product.price,
		initialAvailability: product.stock
	}));
	res.json(formattedProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId);
	const product = getItemById(itemId);

	if (!product) {
		return res.status(404).json({ status: 'Product not found' });
	}

	const reservedStock = await getCurrentReservedStockById(itemId);
	const currentQuantity = product.stock - reservedStock;

	res.json({
		itmeId: product.itemId,
		itemName: product.itemName,
		price: product.price,
		initialAvailableQuantity: product.stock,
		currentQuantity: currentQuantity
	});
});

app.get('/reserve_product/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId);
	const product = getItemById(itemId);

	if (!product) {
		return res.status(404).json({ status: 'Product not found' });
	}

	const reservedStock = await getCurrentReservedStockById(itemId);
	const currentQuantity = product.stock - reservedStock;

	if (currentQuantity < 1) {
		return res.json({ status: 'Not enough stock available', itemId: itemId });
	}

	await reserveStockById(itemId, reservedStock + 1);

	res.json({ status: 'Reservation confirmed', itemId: itemId });
});

const PORT = 1245;
app.listen(PORT, () => {
	console.log(`Server is running on port ${PORT}`);
});
