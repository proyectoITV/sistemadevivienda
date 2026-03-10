from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0018_colacorreos'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogosMarcas',
            fields=[
                ('idmarca', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre de la marca', max_length=150, unique=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción adicional')),
                ('activo', models.BooleanField(default=True, help_text='¿La marca está activa?')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'db_table': 'catalogos_marcas',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PatrimonioClasificacionContraloria',
            fields=[
                ('idclasificacion_contraloria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre de la clasificación de Contraloría', max_length=150, unique=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción adicional')),
                ('activo', models.BooleanField(default=True, help_text='¿La clasificación está activa?')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Clasificación de Contraloría',
                'verbose_name_plural': 'Clasificaciones de Contraloría',
                'db_table': 'patrimonio_clasificacioncontraloria',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PatrimonioClasificacionSerap',
            fields=[
                ('idclasificacion_serap', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre de la clasificación SERAP', max_length=150, unique=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción adicional')),
                ('activo', models.BooleanField(default=True, help_text='¿La clasificación está activa?')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Clasificación SERAP',
                'verbose_name_plural': 'Clasificaciones SERAP',
                'db_table': 'patrimonio_clasificacionserap',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PatrimonioProveedor',
            fields=[
                ('idproveedor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre del proveedor', max_length=200, unique=True)),
                ('rfc', models.CharField(blank=True, help_text='RFC del proveedor', max_length=13, unique=True)),
                ('telefono', models.CharField(blank=True, help_text='Teléfono del proveedor', max_length=20)),
                ('correo', models.EmailField(blank=True, help_text='Correo del proveedor', max_length=254)),
                ('domicilio', models.TextField(blank=True, help_text='Domicilio del proveedor')),
                ('persona_contacto', models.CharField(blank=True, help_text='Persona de contacto', max_length=200)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción adicional')),
                ('activo', models.BooleanField(default=True, help_text='¿El proveedor está activo?')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'db_table': 'patrimonio_proveedor',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PatrimonioBienesDelInstituto',
            fields=[
                ('idbien', models.AutoField(primary_key=True, serialize=False)),
                ('numero_inventario_itavu', models.CharField(help_text='Número de inventario ITAVU', max_length=50, unique=True)),
                ('numero_inventario_gobierno', models.CharField(blank=True, help_text='Número de inventario Gobierno', max_length=50)),
                ('descripcion', models.CharField(help_text='Descripción del bien', max_length=255)),
                ('fotografia', models.ImageField(blank=True, help_text='Fotografía del bien', null=True, upload_to='patrimonio/fotos/')),
                ('fecha_registro', models.DateField(auto_now_add=True, help_text='Fecha de registro')),
                ('modelo', models.CharField(blank=True, help_text='Modelo del bien', max_length=100)),
                ('serie', models.CharField(blank=True, help_text='Número de serie', max_length=100, unique=True)),
                ('fecha_factura', models.DateField(blank=True, help_text='Fecha de facturación', null=True)),
                ('numero_factura', models.CharField(blank=True, help_text='Número de factura', max_length=50, unique=True)),
                ('costo_articulo', models.DecimalField(decimal_places=2, help_text='Costo del artículo', max_digits=12)),
                ('observaciones', models.TextField(blank=True, help_text='Observaciones sobre el bien')),
                ('activo', models.BooleanField(default=True, help_text='¿El bien está en inventario activo?')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('usuario_captura', models.CharField(blank=True, help_text='Usuario que capturó el registro', max_length=100)),
                ('usuario_modificacion', models.CharField(blank=True, help_text='Usuario que modificó el registro', max_length=100)),
                ('clasificacion_contraloria', models.ForeignKey(blank=True, help_text='Clasificación de Contraloría', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.patrimonioclasificacioncontraloria')),
                ('clasificacion_serap', models.ForeignKey(blank=True, help_text='Clasificación SERAP', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.patrimonioclasificacionserap')),
                ('marca', models.ForeignKey(blank=True, help_text='Marca del bien', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.catalogosmarcas')),
                ('proveedor', models.ForeignKey(blank=True, help_text='Proveedor del bien', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.patrimonioproveedor')),
            ],
            options={
                'verbose_name': 'Bien del Instituto',
                'verbose_name_plural': 'Bienes del Instituto',
                'db_table': 'patrimonio_bienes_del_instituto',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.AddIndex(
            model_name='patrimoniobienesdelinstituto',
            index=models.Index(fields=['numero_inventario_itavu'], name='patri_bien_itavu_idx'),
        ),
        migrations.AddIndex(
            model_name='patrimoniobienesdelinstituto',
            index=models.Index(fields=['numero_inventario_gobierno'], name='patri_bien_gob_idx'),
        ),
        migrations.AddIndex(
            model_name='patrimoniobienesdelinstituto',
            index=models.Index(fields=['activo'], name='patri_bien_activo_idx'),
        ),
    ]
