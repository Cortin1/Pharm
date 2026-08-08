import re

with open("app/src/main/java/com/example/ui/HomeScreen.kt", "r") as f:
    content = f.read()

# Let's just create a completely new UI and overwrite it instead of regex since the user wants a full rewrite.
