import re

with open('app/src/main/java/com/example/ui/DetailScreen.kt', 'r') as f:
    content = f.read()

old_box2 = '''            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(380.dp)
                    .clip(RoundedCornerShape(bottomStart = 48.dp, bottomEnd = 48.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant),'''

new_box2 = '''            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(350.dp)
                    .clip(RoundedCornerShape(bottomStart = 48.dp, bottomEnd = 48.dp))
                    .background(MaterialTheme.colorScheme.secondaryContainer),'''

content = content.replace(old_box2, new_box2)

with open('app/src/main/java/com/example/ui/DetailScreen.kt', 'w') as f:
    f.write(content)
