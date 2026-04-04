from django.forms import ModelForm, TextInput,  NumberInput, ClearableFileInput, DateInput
from shopapp.models import Article, Family, Seller, Purchase
from django.utils.timezone import now
from .models import Purchase


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        labels = {
            "name": "Nombre",
            "family": "Familia",
            "quantity": "Contenido",
            "unit": "Unidad",
            "package": "Paquete",
            "ean": "Código EAN",
            "photo": "Imagen",
        }
        widgets = {
            "name": TextInput(attrs={"placeholder": "NOMBRE"}),
            "quantity": NumberInput(attrs={"placeholder": "CANTIDAD"}),
            "package": NumberInput(attrs={"placeholder": "PAQUETE"}),
            "ean": TextInput(attrs={"placeholder": "CÓDIGO EAN"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

        # ✅ Force placeholder for Family
        self.fields["family"].queryset = Family.objects.all().order_by("name")
        self.fields["family"].empty_label = "Seleccione una familia"
        self.fields["family"].required = True

        # ✅ Unit already working
        self.fields["unit"].choices = [("", "Seleccione unidad")] + list(self.fields["unit"].choices)
        self.fields["unit"].required = True


class SellerForm(ModelForm):
    class Meta:
        model=Seller
        fields = "__all__"
        labels = {
            "name" : "Nombre",
            "photo" : "Imagen"
        }
        widgets = {
            "name": TextInput(attrs={"placeholder": "NOMBRE"}),
            "photo": ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

        self.fields["name"].required = True

class PurchaseForm(ModelForm):
    class Meta:
        model=Purchase
        fields = "__all__"
        labels = {
            "date" : "Fecha",
            "quantity" : "Cantidad",
            "article" : "Articulo",
            "price" : "Precio",
            "note" : "Nota",
            "seller" : "Tienda",
        }
        widgets = {
            "date": DateInput(format="%Y-%m-%d",attrs={"type": "date"}),
            "quantity": NumberInput(attrs={"placeholder": "CANTIDAD"}),
            "price": NumberInput(attrs={"placeholder": "PRECIO"}),
            "note": TextInput(attrs={"placeholder": "NOTAS"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

        # Default date logic. set initial date to the last purchase date or to today if no purchases exist
        if "date" in self.initial:
            self.fields["date"].initial = self.initial["date"]
        else:
            last_purchase = Purchase.objects.order_by("-date").first()
            if last_purchase:
                self.fields["date"].initial = last_purchase.date
            else:
                self.fields["date"].initial = now().date()

        # set autofocus on quantity field since date es almost always correct and article is selected after quantity
        self.fields["quantity"].widget.attrs["autofocus"] = True

        # ✅ Force placeholder for Article
        self.fields["article"].queryset = Article.objects.all().order_by("name")
        self.fields["article"].empty_label = "Seleccione un articulo"
        self.fields["article"].required = True

        # ✅ Force placeholder for Seller
        self.fields["seller"].queryset = Seller.objects.all().order_by("name")
        self.fields["seller"].empty_label = "Seleccione una tienda"
        self.fields["seller"].required = True

       