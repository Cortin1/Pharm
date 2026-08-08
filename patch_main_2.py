import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_home = '''            HomeScreen(
                viewModel = viewModel,
                onNavigateToAdd = { navController.navigate("add") },
                onNavigateToDetail = { id -> navController.navigate("detail/$id") }
            )'''

new_home = '''            HomeScreen(
                viewModel = viewModel,
                onNavigateToAdd = { navController.navigate("add") },
                onNavigateToDetail = { id -> navController.navigate("detail/$id") },
                onNavigateToDashboard = { navController.navigate("dashboard") }
            )'''

content = content.replace(old_home, new_home)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
