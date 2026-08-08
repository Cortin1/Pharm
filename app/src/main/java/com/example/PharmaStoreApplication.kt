package com.example

import android.app.Application
import com.example.data.AppDatabase
import com.example.data.ProductRepository

class PharmaStoreApplication : Application() {
    val database by lazy { AppDatabase.getDatabase(this) }
    val repository by lazy { ProductRepository(database.productDao(), database.stockTransactionDao()) }
}
