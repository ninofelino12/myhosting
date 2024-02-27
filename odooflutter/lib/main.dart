import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class _MyAppState extends State<MyApp> {
  final productBloc = ProductBloc(productData); // Instantiate the BloC

  @override
  void dispose() {
    productBloc.close(); // Close the BloC when the widget is disposed
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Product Data'),
          actions: [
            PopupMenuButton(
              onSelected: (value) {
                productBloc
                    .add(LoadProductData(value as int)); // Dispatch event
              },
              itemBuilder: (context) => [
                for (int i = 0; i < jsonUrls.length; i++)
                  PopupMenuItem(
                    value: i,
                    child: Text('Data Set ${i + 1}'),
                  ),
              ],
            ),
          ],
        ),
        body: BlocBuilder<ProductBloc, ProductState>(
          bloc: productBloc,
          builder: (context, state) {
            if (state is ProductLoading) {
              return Center(child: CircularProgressIndicator());
            } else if (state is ProductLoaded) {
              final products = state.products;
              return GridView.builder(
                  // ... same as before, using products from state
                  );
            } else if (state is ProductError) {
              return Center(text: Text(state.message));
            } else {
              return SizedBox(); // Handle unexpected states
            }
          },
        ),
      ),
    );
  }
}
