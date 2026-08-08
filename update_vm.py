with open("app/src/main/java/com/example/ui/ProductViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("val transactions:", """val totalStock = kotlinx.coroutines.flow.map { list: List<Product> -> list.sumOf { it.quantity } }(repository.allProducts)
    val outOfStockCount = kotlinx.coroutines.flow.map { list: List<Product> -> list.count { it.quantity == 0 } }(repository.allProducts)
    val recentTransactions = kotlinx.coroutines.flow.map { list: List<StockTransaction> -> list.take(10) }(repository.allTransactions)

    val transactions:""")
    
with open("app/src/main/java/com/example/ui/ProductViewModel.kt", "w") as f:
    f.write(content)
