import re

with open('app/src/main/java/com/example/ui/DashboardScreen.kt', 'r') as f:
    content = f.read()

old_call = '''    val dateFormatter = SimpleDateFormat("MM/yyyy", Locale.getDefault())
    val currentDate = Date()
    val expiringCount = products.count { 
        it.expirationDate.isNotBlank() && isExpiringSoon(it.expirationDate, currentDate, dateFormatter)
    }'''

new_call = '''    val currentDate = Date()
    val expiringCount = products.count { 
        it.expirationDate.isNotBlank() && isExpiringSoon(it.expirationDate, currentDate)
    }'''

content = content.replace(old_call, new_call)

old_fun = '''fun isExpiringSoon(expirationDateStr: String, currentDate: Date, format: SimpleDateFormat): Boolean {
    try {
        val expDate = format.parse(expirationDateStr)'''

new_fun = '''fun isExpiringSoon(expirationDateStr: String, currentDate: Date): Boolean {
    try {
        val format = if (expirationDateStr.length == 5) SimpleDateFormat("MM/yy", Locale.getDefault()) else SimpleDateFormat("MM/yyyy", Locale.getDefault())
        val expDate = format.parse(expirationDateStr)'''

content = content.replace(old_fun, new_fun)

with open('app/src/main/java/com/example/ui/DashboardScreen.kt', 'w') as f:
    f.write(content)
