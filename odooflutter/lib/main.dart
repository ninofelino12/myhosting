import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String _productProductData = '';
  String _productTemplateData = '';

  Future<void> _fetchData() async {
    final productProductResponse = await http
        .get(Uri.parse('http://localhost:5000/product/product.category/1'));
    final productTemplateResponse = await http
        .get(Uri.parse('http://localhost:5000/product/product.category/1'));

    if (productProductResponse.statusCode == 200 &&
        productTemplateResponse.statusCode == 200) {
      setState(() {
        _productProductData =
            json.decode(productProductResponse.body).toString();
        _productTemplateData =
            json.decode(productTemplateResponse.body).toString();
      });
    } else {
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Display JSON Data'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              ElevatedButton(
                onPressed: _fetchData,
                child: Text('Fetch Data'),
              ),
              SizedBox(height: 20),
              Text('Product Product Data: $_productProductData'),
              SizedBox(height: 20),
              Text('Product Template Data: $_productTemplateData'),
            ],
          ),
        ),
      ),
    );
  }
}
