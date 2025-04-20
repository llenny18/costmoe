from django.db import models


class AiRecommendations(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    searched_product = models.CharField(max_length=255, blank=True, null=True)
    recommended_product = models.CharField(max_length=255, blank=True, null=True)
    confidence_level = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    generated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ai_recommendations'


class ExtractedQuotationData(models.Model):
    extracted_id = models.AutoField(primary_key=True)
    quotation_id = models.IntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    supplier_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extracted_quotation_data'


class MarketReports(models.Model):
    report_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    report_file = models.CharField(max_length=255, blank=True, null=True)
    report_path = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'market_reports'


class Notifications(models.Model):
    STATUS_CHOICES = (
        ('unread', 'Unread'),
        ('read', 'Read'),
    )
    
    notification_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='unread', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class ProductGroups(models.Model):

    id = models.AutoField(primary_key=True)
    group_id = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'product_groups'


class Products(models.Model):
    AVAILABILITY_CHOICES = (
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    )
    
    SOURCE_WEBSITE_CHOICES = (
        ('Shopee', 'Shopee'),
        ('Lazada', 'Lazada'),
        ('Zalora', 'Zalora'),
        ('Carousell', 'Carousell'),
        ('TikTok Shop', 'TikTok Shop'),
        ('PhilGEPS', 'PhilGEPS'),
        ('Citimart', 'Citimart'),
        ('Amazon', 'Amazon'),
        ('eBay', 'eBay'),
        ('AliExpress', 'AliExpress'),
        ('Rakuten', 'Rakuten'),
        ('Temu', 'Temu'),
        ('Galleon', 'Galleon'),
        ('BeautyMNL', 'BeautyMNL'),
    )
    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES, blank=True, null=True)
    source_website = models.CharField(max_length=15, choices=SOURCE_WEBSITE_CHOICES, blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    user_id = models.CharField(max_length=200, blank=True, null=True)
    group_id = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


from django.db import models

class BestProductsPerGroup(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    user_id = models.IntegerField()
    group_id = models.IntegerField()
    rank_in_group = models.IntegerField()
    availability = models.CharField(max_length=50)
    source_website = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    source_url = models.URLField(max_length=500, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    # Computed fields from the view
    final_score = models.FloatField()
    why_scored = models.TextField()

    class Meta:
        managed = False  # This is a view, not a Django-managed table
        db_table = 'RankedProductsPerGroup'


class ProductHistory(models.Model):
    AVAILABILITY_CHOICES = (
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    )
    
    history_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES, blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_history'


class ProductPriceBySource(models.Model):
    SOURCE_WEBSITE_CHOICES = (
        ('Shopee', 'Shopee'),
        ('Lazada', 'Lazada'),
        ('Zalora', 'Zalora'),
        ('Carousell', 'Carousell'),
        ('TikTok Shop', 'TikTok Shop'),
        ('PhilGEPS', 'PhilGEPS'),
        ('Citimart', 'Citimart'),
        ('Amazon', 'Amazon'),
        ('eBay', 'eBay'),
        ('AliExpress', 'AliExpress'),
        ('Rakuten', 'Rakuten'),
        ('Temu', 'Temu'),
        ('Galleon', 'Galleon'),
        ('BeautyMNL', 'BeautyMNL'),
    )
    
    source_website = models.CharField(max_length=15, choices=SOURCE_WEBSITE_CHOICES, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.CharField(max_length=100, blank=True, null=True)
    product_count = models.BigIntegerField(blank=True, null=True)
    avg_price = models.DecimalField(max_digits=14, decimal_places=6, blank=True, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_price_by_source'


class Quotations(models.Model):
    quotation_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quotations'


class SystemLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    action = models.TextField(blank=True, null=True)
    log_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_logs'


class Users(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('business_owner', 'Business Owner'),
        ('customer', 'Customer'),
    )
    
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=14, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'