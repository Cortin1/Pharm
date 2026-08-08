content = """package com.example.ui

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.AddAPhoto
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import coil.compose.AsyncImage
import com.example.utils.ImageUtils
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.text.input.TransformedText
import androidx.compose.ui.text.input.OffsetMapping
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.graphics.Color
import java.io.File

class DateTransformation : VisualTransformation {
    override fun filter(text: AnnotatedString): TransformedText {
        val trimmed = if (text.text.length >= 6) text.text.substring(0..5) else text.text
        var out = ""
        for (i in trimmed.indices) {
            out += trimmed[i]
            if (i == 1) out += "/"
        }
        val dateOffsetTranslator = object : OffsetMapping {
            override fun originalToTransformed(offset: Int): Int {
                if (offset <= 1) return offset
                if (offset <= 6) return offset + 1
                return 7
            }
            override fun transformedToOriginal(offset: Int): Int {
                if (offset <= 2) return offset
                if (offset <= 7) return offset - 1
                return 6
            }
        }
        return TransformedText(AnnotatedString(out), dateOffsetTranslator)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddProductScreen(
    productId: Int? = null,
    viewModel: ProductViewModel,
    onNavigateBack: () -> Unit
) {
    val products by viewModel.products.collectAsStateWithLifecycle()
    val productToEdit = remember(productId, products) { products.find { it.id == productId } }

    var name by remember { mutableStateOf("") }
    var otherNames by remember { mutableStateOf("") }
    var location by remember { mutableStateOf("Magasin 1") }
    var quantity by remember { mutableStateOf("") }
    var expirationDate by remember { mutableStateOf(TextFieldValue("")) }
    var selectedImageUri by remember { mutableStateOf<Uri?>(null) }
    var existingImagePath by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(productToEdit) {
        productToEdit?.let {
            name = it.name
            otherNames = it.otherNames
            location = it.location
            quantity = it.quantity.toString()
            val dateStr = it.expirationDate.replace("/", "")
            expirationDate = TextFieldValue(text = dateStr, selection = TextRange(dateStr.length))
            existingImagePath = it.imagePath
        }
    }

    val context = LocalContext.current
    val photoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.PickVisualMedia(),
        onResult = { uri -> selectedImageUri = uri }
    )

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        if (productId == null) "New Item" else "Edit Item",
                        fontWeight = FontWeight.Bold
                    ) 
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 24.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            // Image Picker
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant)
                    .clickable {
                        photoPickerLauncher.launch(
                            PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                        )
                    },
                contentAlignment = Alignment.Center
            ) {
                if (selectedImageUri != null) {
                    AsyncImage(
                        model = selectedImageUri,
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else if (existingImagePath != null) {
                    AsyncImage(
                        model = File(existingImagePath!!),
                        contentDescription = null,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.AddAPhoto,
                            contentDescription = null,
                            modifier = Modifier.size(48.dp),
                            tint = MaterialTheme.colorScheme.primary
                        )
                        Spacer(Modifier.height(8.dp))
                        Text(
                            "Add a photo",
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.primary
                        )
                    }
                }
            }

            StyledTextField(
                value = name,
                onValueChange = { name = it },
                label = "Product Name"
            )

            StyledTextField(
                value = otherNames,
                onValueChange = { otherNames = it },
                label = "Other Names / Categories"
            )

            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                StyledTextField(
                    value = quantity,
                    onValueChange = { if (it.all { char -> char.isDigit() }) quantity = it },
                    label = "Quantity",
                    modifier = Modifier.weight(1f)
                )
                OutlinedTextField(
                    value = expirationDate,
                    onValueChange = { if (it.text.length <= 6 && it.text.all { char -> char.isDigit() }) expirationDate = it },
                    label = { Text("Exp (MMYYYY)") },
                    modifier = Modifier.weight(1f),
                    visualTransformation = DateTransformation(),
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.surface,
                        unfocusedContainerColor = MaterialTheme.colorScheme.surface
                    )
                )
            }

            Text(
                "Select Location",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onBackground
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                listOf("Magasin 1", "Magasin 2", "Magasin 3").forEach { loc ->
                    val isSelected = location == loc
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(16.dp))
                            .background(
                                if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface
                            )
                            .clickable { location = loc }
                            .padding(vertical = 12.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = loc,
                            color = if (isSelected) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            Spacer(Modifier.height(24.dp))

            Button(
                onClick = {
                    val finalImagePath = selectedImageUri?.let { uri ->
                        ImageUtils.saveImageToInternalStorage(context, uri)
                    } ?: existingImagePath

                    val formattedDate = if (expirationDate.text.length == 6) {
                        "${expirationDate.text.substring(0..1)}/${expirationDate.text.substring(2..5)}"
                    } else {
                        expirationDate.text
                    }

                    if (productId != null && productToEdit != null) {
                        val originalQuantity = productToEdit.quantity
                        val newQuantity = quantity.toIntOrNull() ?: 0
                        viewModel.updateProduct(
                            productToEdit.copy(
                                name = name,
                                otherNames = otherNames,
                                location = location,
                                quantity = newQuantity,
                                expirationDate = formattedDate,
                                imagePath = finalImagePath
                            )
                        )
                        if (newQuantity != originalQuantity) {
                            val diff = newQuantity - originalQuantity
                            val type = if (diff > 0) "IN" else "OUT"
                            viewModel.recordTransaction(productToEdit.id, name, type, kotlin.math.abs(diff))
                        }
                    } else {
                        viewModel.addProduct(
                            name = name,
                            otherNames = otherNames,
                            location = location,
                            quantity = quantity.toIntOrNull() ?: 0,
                            expirationDate = formattedDate,
                            imagePath = finalImagePath
                        )
                        if ((quantity.toIntOrNull() ?: 0) > 0) {
                            // Initial stock recorded as transaction isn't perfect, but let's assume we do if needed.
                        }
                    }
                    onNavigateBack()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                shape = RoundedCornerShape(16.dp),
                enabled = name.isNotBlank() && quantity.isNotBlank()
            ) {
                Text(
                    if (productId == null) "Save Item" else "Update Item",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
            }
            
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
fun StyledTextField(
    value: String,
    onValueChange: (String) -> Unit,
    label: String,
    modifier: Modifier = Modifier
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        label = { Text(label) },
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = MaterialTheme.colorScheme.surface,
            unfocusedContainerColor = MaterialTheme.colorScheme.surface
        )
    )
}
"""
with open("app/src/main/java/com/example/ui/AddProductScreen.kt", "w") as f:
    f.write(content)
