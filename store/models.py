from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models


class Collection(models.Model):
    """
    Набор / коллекция:
    title - название коллекции
    """
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    """
    Акция:
    description - описание акции
    start_date - дата начала акции
    end_date - дата окончания акции
    discount - скидка
    """
    description = models.CharField(max_length=255)
    start_date = models.DateField(auto_now=True)
    end_date = models.DateField(auto_now=True)
    discount = models.FloatField()


class Product(models.Model):
    """
    Продукт:
    title - наименование продукта
    slug
    description - описание продукта
    unit_price - стоимость за единицу товара
    inventory - количество единиц на складе
    last_update - последнее обновление записи
    collection - id коллекции, к которой относится товар
    promotions - id акции, к которой относится товар
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,
                                   on_delete=models.PROTECT,
                                   related_name='products')  # потребуется удалить все продукты, лежащие в коллекции
    # чтобы удалить коллекцию
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    """
    Покупатель
    first_name - имя
    last_name - фамилия
    email - адрес почты
    phone - номер телефона
    birth_date - дата дня рождения
    membership - уровень членства
    """
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = (
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    """
    Заказ
    placed_at - дата оформления
    payment_status - статус заказа
    customer - покупатель
    """
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    )

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.PROTECT)  # если покупатель будет удалён, информация о заказах сохранится


class OrderItem(models.Model):
    """
    Элемент заказа
    order - заказ
    product - товар
    quantity - количество
    unit_price - стоимость элемента заказа
    """
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)


class Address(models.Model):
    """
    Адрес
    customer - покупатель
    street - улица
    city - город
    zip - почтовый индекс

    Каждый покупатель в системе характеризуется адресом (и он единственен).
    В силу того, что в отношении Покупатель - Адрес родителем является покупатель
    (он должен быть создан раньше адреса), то ForeignKey заводится в модели Адрес

    on_delete определяет, как должна вести себя дочерняя модель, если родитель будет удален
    * models.CASCADE - удалить запись дочерних моделей
    * models.SET_NULL - выставить значение поля в NULL
    * models.PROTECT - потребуется удаление всех детей перед удалением родителя
    * models.SET_DEFAULT - выставить значение по умолчанию
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=20, null=True)


class Cart(models.Model):
    """
    Корзина
    created_at - дата создания
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    """
    CartItem - элемент корзины
    cart - корзина
    product - продукт
    quantity - количество
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [
            ['cart', 'product'] # исключаем возможность наличия в корзине одинаковых продуктов
        ]

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
