package com.example.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface StockTransactionDao {
    @Insert
    suspend fun insertTransaction(transaction: StockTransaction)

    @Query("SELECT * FROM stock_transactions ORDER BY date DESC")
    fun getAllTransactions(): Flow<List<StockTransaction>>
    
    @Query("SELECT * FROM stock_transactions WHERE productId = :productId ORDER BY date DESC")
    fun getTransactionsForProduct(productId: Int): Flow<List<StockTransaction>>
}
