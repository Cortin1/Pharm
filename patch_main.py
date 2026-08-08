import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'import com.example.ui.HomeScreen',
    'import com.example.ui.HomeScreen\nimport com.example.ui.DashboardScreen'
)

old_nav = '''        composable("add") {
            AddProductScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }'''

new_nav = '''        composable("add") {
            AddProductScreen(
                productId = null,
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable(
            route = "edit/{id}",
            arguments = listOf(navArgument("id") { type = NavType.IntType })
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getInt("id")
            AddProductScreen(
                productId = id,
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
        composable("dashboard") {
            DashboardScreen(
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }'''

content = content.replace(old_nav, new_nav)

old_detail = '''            DetailScreen(
                productId = id,
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() }
            )'''
            
new_detail = '''            DetailScreen(
                productId = id,
                viewModel = viewModel,
                onNavigateBack = { navController.popBackStack() },
                onNavigateToEdit = { editId -> navController.navigate("edit/$editId") }
            )'''

content = content.replace(old_detail, new_detail)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
