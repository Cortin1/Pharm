import re

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'r') as f:
    content = f.read()

old_save = """                        if (productId == null) {
                            viewModel.addProduct(
                                name = name.trim(),
                                otherNames = otherNames.trim(),
                                location = location.trim(),
                                quantity = qty,
                                expirationDate = expirationDate.trim(),
                                imagePath = imagePath
                            )
                        } else {
                            productToEdit?.let {
                                viewModel.updateProduct(it.copy(
                                    name = name.trim(),
                                    otherNames = otherNames.trim(),
                                    location = location.trim(),
                                    quantity = qty,
                                    expirationDate = expirationDate.trim(),
                                    imagePath = imagePath
                                ))
                            }
                        }"""

new_save = """                        val expText = expirationDate.text.trim()
                        val formattedDate = if (expText.length == 4) {
                            "${expText.substring(0, 2)}/${expText.substring(2, 4)}"
                        } else {
                            expText
                        }
                        
                        if (productId == null) {
                            viewModel.addProduct(
                                name = name.trim(),
                                otherNames = otherNames.trim(),
                                location = location.trim(),
                                quantity = qty,
                                expirationDate = formattedDate,
                                imagePath = imagePath
                            )
                        } else {
                            productToEdit?.let {
                                viewModel.updateProduct(it.copy(
                                    name = name.trim(),
                                    otherNames = otherNames.trim(),
                                    location = location.trim(),
                                    quantity = qty,
                                    expirationDate = formattedDate,
                                    imagePath = imagePath
                                ))
                            }
                        }"""

content = content.replace(old_save, new_save)

with open('app/src/main/java/com/example/ui/AddProductScreen.kt', 'w') as f:
    f.write(content)
