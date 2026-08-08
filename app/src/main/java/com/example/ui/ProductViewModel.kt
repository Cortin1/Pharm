package com.example.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.Product
import com.example.data.ProductRepository
import com.example.data.StockTransaction
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class ProductViewModel(private val repository: ProductRepository) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery

    @OptIn(ExperimentalCoroutinesApi::class)
    val products: StateFlow<List<Product>> = _searchQuery
        .flatMapLatest { query ->
            if (query.isBlank()) {
                repository.allProducts
            } else {
                repository.searchProducts(query)
            }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    val totalStock: StateFlow<Int> = repository.allProducts
        .map { list -> list.sumOf { it.quantity } }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), 0)

    val outOfStockCount: StateFlow<Int> = repository.allProducts
        .map { list -> list.count { it.quantity == 0 } }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), 0)

    val recentTransactions: StateFlow<List<StockTransaction>> = repository.allTransactions
        .map { list -> list.take(10) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val transactions: StateFlow<List<StockTransaction>> = repository.allTransactions
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    fun onSearchQueryChanged(query: String) {
        _searchQuery.value = query
    }

    fun addProduct(name: String, otherNames: String, location: String, quantity: Int, expirationDate: String, imagePath: String?) {
        viewModelScope.launch {
            repository.insert(Product(
                name = name, 
                otherNames = otherNames,
                location = location,
                quantity = quantity,
                expirationDate = expirationDate,
                imagePath = imagePath
            ))
        }
    }

    fun updateProduct(product: Product) {
        viewModelScope.launch {
            repository.update(product)
        }
    }

    fun recordTransaction(productId: Int, productName: String, type: String, quantity: Int) {
        viewModelScope.launch {
            repository.recordTransaction(
                StockTransaction(
                    productId = productId,
                    productName = productName,
                    type = type,
                    quantity = quantity
                )
            )
        }
    }

    fun deleteProduct(id: Int) {
        viewModelScope.launch {
            repository.deleteById(id)
        }
    }
}

class ProductViewModelFactory(private val repository: ProductRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ProductViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ProductViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
