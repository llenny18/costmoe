# Generated by Django 5.1.6 on 2025-04-14 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AiRecommendations',
            fields=[
                ('recommendation_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('searched_product', models.CharField(blank=True, max_length=255, null=True)),
                ('recommended_product', models.CharField(blank=True, max_length=255, null=True)),
                ('confidence_level', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('generated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ai_recommendations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExtractedQuotationData',
            fields=[
                ('extracted_id', models.AutoField(primary_key=True, serialize=False)),
                ('quotation_id', models.IntegerField(blank=True, null=True)),
                ('product_name', models.CharField(blank=True, max_length=255, null=True)),
                ('specifications', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('supplier_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'extracted_quotation_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MarketReports',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('report_file', models.CharField(blank=True, max_length=255, null=True)),
                ('report_path', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'market_reports',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('unread', 'Unread'), ('read', 'Read')], default='unread', max_length=6, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'notifications',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductHistory',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('availability', models.CharField(blank=True, choices=[('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], max_length=12, null=True)),
                ('recorded_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'product_history',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductPriceBySource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_website', models.CharField(blank=True, choices=[('Shopee', 'Shopee'), ('Lazada', 'Lazada'), ('Zalora', 'Zalora'), ('Carousell', 'Carousell'), ('TikTok Shop', 'TikTok Shop'), ('PhilGEPS', 'PhilGEPS'), ('Citimart', 'Citimart'), ('Amazon', 'Amazon'), ('eBay', 'eBay'), ('AliExpress', 'AliExpress'), ('Rakuten', 'Rakuten'), ('Temu', 'Temu'), ('Galleon', 'Galleon'), ('BeautyMNL', 'BeautyMNL')], max_length=15, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated', models.CharField(blank=True, max_length=100, null=True)),
                ('product_count', models.BigIntegerField(blank=True, null=True)),
                ('avg_price', models.DecimalField(blank=True, decimal_places=6, max_digits=14, null=True)),
                ('min_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('avg_rating', models.DecimalField(blank=True, decimal_places=6, max_digits=7, null=True)),
            ],
            options={
                'db_table': 'product_price_by_source',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(blank=True, max_length=10, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('availability', models.CharField(blank=True, choices=[('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], max_length=12, null=True)),
                ('source_website', models.CharField(blank=True, choices=[('Shopee', 'Shopee'), ('Lazada', 'Lazada'), ('Zalora', 'Zalora'), ('Carousell', 'Carousell'), ('TikTok Shop', 'TikTok Shop'), ('PhilGEPS', 'PhilGEPS'), ('Citimart', 'Citimart'), ('Amazon', 'Amazon'), ('eBay', 'eBay'), ('AliExpress', 'AliExpress'), ('Rakuten', 'Rakuten'), ('Temu', 'Temu'), ('Galleon', 'Galleon'), ('BeautyMNL', 'BeautyMNL')], max_length=15, null=True)),
                ('source_url', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Quotations',
            fields=[
                ('quotation_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
                ('file_path', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'quotations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SystemLogs',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('action', models.TextField(blank=True, null=True)),
                ('log_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'system_logs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
                ('password_hash', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('analyst', 'Analyst'), ('business_owner', 'Business Owner'), ('customer', 'Customer')], max_length=14)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
