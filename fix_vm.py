import re
with open("app/src/main/java/com/example/ui/ProductViewModel.kt", "r") as f:
    content = f.read()

content = content.replace("val totalStock = kotlinx.coroutines.flow.map { list: List<Product> -> list.sumOf { it.quantity } }(repository.allProducts)", "val totalStock = kotlinx.coroutines.flow.map { it.sumOf { p -> p.quantity } }(repository.allProducts)")
content = content.replace("val outOfStockCount = kotlinx.coroutines.flow.map { list: List<Product> -> list.count { it.quantity == 0 } }(repository.allProducts)", "val outOfStockCount = kotlinx.coroutines.flow.map { it.count { p -> p.quantity == 0 } }(repository.allProducts)")
content = content.replace("val recentTransactions = kotlinx.coroutines.flow.map { list: List<StockTransaction> -> list.take(10) }(repository.allTransactions)", "val recentTransactions = kotlinx.coroutines.flow.map { it.take(10) }(repository.allTransactions)")

# Wait, the correct syntax in kotlin for extension functions is `repository.allProducts.map { it.sumOf { ... } }`
import sys
with open("app/src/main/java/com/example/ui/ProductViewModel.kt", "w") as f:
    # rewrite from scratch to ensure correct imports
    pass
