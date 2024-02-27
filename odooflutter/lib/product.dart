class Product {
  final int id;
  final String name;
  // ... other properties

  Product(this.id, this.name);

  factory Product.fromJson(Map<String, dynamic> json) => Product(
        json['id'],
        json['name'],
      );
}
