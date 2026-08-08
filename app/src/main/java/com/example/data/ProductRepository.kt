package com.example.data

import kotlinx.coroutines.flow.Flow

class ProductRepository(
    private val productDao: ProductDao,
    private val transactionDao: StockTransactionDao
) {
    val allProducts: Flow<List<Product>> = productDao.getAllProducts()
    val allTransactions: Flow<List<StockTransaction>> = transactionDao.getAllTransactions()

    fun searchProducts(query: String): Flow<List<Product>> {
        return productDao.searchProducts(query)
    }
    
    suspend fun getProductById(id: Int): Product? {
        return productDao.getProductById(id)
    }

    suspend fun insert(product: Product) {
        productDao.insertProduct(product)
    }

    suspend fun update(product: Product) {
        productDao.updateProduct(product)
    }

    suspend fun deleteById(id: Int) {
        productDao.deleteProductById(id)
    }

    suspend fun recordTransaction(transaction: StockTransaction) {
        transactionDao.insertTransaction(transaction)
    }
}
