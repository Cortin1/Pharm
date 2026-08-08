import re

with open('app/src/main/java/com/example/ui/HomeScreen.kt', 'r') as f:
    content = f.read()

old_actions = '''                actions = {
                    IconButton(onClick = onNavigateToDashboard) {
                        Icon(Icons.Default.Analytics, contentDescription = "Dashboard", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    IconButton(onClick = { 
                        // Seed mock data
                        viewModel.addProduct("Paracétamol 500mg", "Doliprane, Acetaminophen", "Magasin 1", 500, "12/2027", null)
                        viewModel.addProduct("Seringues 5ml", "Seringue jetable", "Magasin 2", 1200, "06/2028", null)
                        viewModel.addProduct("Bandelettes Test", "Test Glycémie", "Magasin 1", 50, "01/2026", null)
                        viewModel.addProduct("Compresses Stériles", "Gaze", "Magasin 3", 800, "10/2030", null)
                    }) {
                        Icon(Icons.Default.Refresh, contentDescription = "Seed Data", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Box('''

new_actions = '''                actions = {
                    IconButton(onClick = onNavigateToDashboard) {
                        Icon(Icons.Default.Analytics, contentDescription = "Dashboard", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Box('''

content = content.replace(old_actions, new_actions)

with open('app/src/main/java/com/example/ui/HomeScreen.kt', 'w') as f:
    f.write(content)
