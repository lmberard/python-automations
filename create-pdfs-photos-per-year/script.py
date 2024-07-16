import os
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas

# Define el tamaño de cada foto y el espacio entre ellas
photo_size = (80, 80)  # tamaño en mm
spacing = 5  # espacio entre fotos en mm

# Convierte mm a puntos (1 mm = 2.83465 puntos)
mm_to_points = 2.83465
photo_size_points = (int(photo_size[0] * mm_to_points), int(photo_size[1] * mm_to_points))
spacing_points = int(spacing * mm_to_points)

# Tamaño de la hoja A3 en puntos
a3_width, a3_height = A3

# Función para agregar fotos a una página PDF
def add_photos_to_canvas(c, photos):
    x, y = spacing_points, a3_height - spacing_points - photo_size_points[1]
    for photo_path in photos:
        img = Image.open(photo_path)
        img = ImageOps.contain(img, photo_size_points, method=Image.Resampling.LANCZOS)  # Mantener la relación de aspecto
        img = ImageOps.expand(img, border=(0, 0, photo_size_points[0] - img.size[0], photo_size_points[1] - img.size[1]), fill='white')  # Añadir bordes blancos
        img_path = photo_path.replace('\\', '/')
        
        # Guardar la imagen temporalmente en alta calidad
        temp_img_path = photo_path + "_temp.jpg"
        img.save(temp_img_path, quality=95)
        
        c.drawImage(temp_img_path, x, y, width=photo_size_points[0], height=photo_size_points[1])
        
        # Eliminar la imagen temporal
        os.remove(temp_img_path)
        
        x += photo_size_points[0] + spacing_points
        if x + photo_size_points[0] + spacing_points > a3_width:
            x = spacing_points
            y -= photo_size_points[1] + spacing_points
            if y < spacing_points:
                c.showPage()
                x, y = spacing_points, a3_height - spacing_points - photo_size_points[1]

# Ruta a la carpeta de fotos
photos_folder = "./"  # Ajusta esta ruta según sea necesario

# Recorrer carpetas y fotos
for year_folder in sorted(os.listdir(photos_folder)):
    year_path = os.path.join(photos_folder, year_folder)
    if os.path.isdir(year_path):
        photos = []
        for photo_file in sorted(os.listdir(year_path)):
            if photo_file.lower().endswith(('jpg', 'jpeg', 'png', 'gif')):
                photos.append(os.path.join(year_path, photo_file))
        
        # Crear un archivo PDF para cada año
        output_pdf_path = os.path.join(photos_folder, f"{year_folder}.pdf")
        c = canvas.Canvas(output_pdf_path, pagesize=A3)
        
        add_photos_to_canvas(c, photos)
        
        c.save()
        print(f"PDF creado para el año {year_folder}: {output_pdf_path}")

print("Proceso completado.")
