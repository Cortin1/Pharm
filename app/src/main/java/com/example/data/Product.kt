package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "products")
data class Product(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val name: String,
    val otherNames: String = "",
    val location: String = "Magasin 1",
    val quantity: Int = 0,
    val expirationDate: String = "",
    val imagePath: String? = null,
    val timestamp: Long = System.currentTimeMillis()
)
