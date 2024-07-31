import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;
const client = createClient();

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

client.on('connect', function() {
	console.log('Redis client connected to the server');
});

client.on('error', (err) => {
	console.log(`Redis client not connected to the server: ${err}`);
});

const listProducts = [
	{'id': 1, 'name': 'Suitcase 250', 'price': 50, 'stock': 4},
	{'id': 2, 'name': 'Suitcase 450', 'price': 100, 'stock': 10},
	{'id': 3, 'name': 'Suitcase 650', 'price': 350, 'stock': 2},
	{'id': 4, 'name': 'Suitcase 1050', 'price': 550, 'stock': 5},
];

function getItemById(id) {
	return listProducts.find(item => item.id == id);
}

function reserveStockById(itemId, stock) {
	// client.set(itemId, stock);
	return setAsync(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
	const stock = await client.get(itemId);
	return stock;
}

app.get('/list_products', (req, res) => {
  return res.status(200).json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId, 10);
	const product = getItemById(itemId);

	if (!product) {
		return res.status(404).json({ status: 'Product not found' });
	}

	const currentQuantity = await getCurrentReservedStockById(itemId);
	const response = {
		itemId: product.id,
		itemName: product.name,
		price: product.price,
		initialAvailableQuantity: product.stock,
        	currentQuantity: currentQuantity !== null ? parseInt(currentQuantity) : product.stock,
	};

    res.status(200).json(response);
});

app.get('/reserve_product/:itemId', async (req, res) => {
	const itemId = parseInt(req.params.itemId, 10);
        const product = getItemById(itemId);

	if (!product) {
                return res.status(404).json({ status: 'Product not found' });
        }

	const currentQuantity = await getCurrentReservedStockById(itemId);
	const availableStock = currentQuantity !== null ? currentQuantity : product.stock;
	if (availableStock < 1) {
		return res.status().json({"status":"Not enough stock available","itemId": itemId});
	}
	await reserveStockById(itemId, availableStock - 1);
	return res.status(200).json({"status":"Reservation confirmed","itemId": itemId});
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
