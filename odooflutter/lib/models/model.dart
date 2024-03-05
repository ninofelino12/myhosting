import 'package:flutter/material.dart';
import 'package:odooflutter/main.dart';

final List<Map<String, String>> menuItems = [
  {'value': 'res.partner', 'text': 'Partner'},
  {'value': 'product.template', 'text': 'Product Template'},
  {'value': 'product.category', 'text': 'Product Category'},
  {'value': 'product.product', 'text': 'Product'},
  {'value': 'ir.module.categoryp', 'text': 'Addons Category'},
  {'value': 'ir.module.module', 'text': 'Addons'},
  {'value': 'ir.actions.report', 'text': 'Report'},
];

class CustomPopupMenuItem extends PopupMenuItem<String> {
  @override
  // ignore: overridden_fields
  final String value;
  final String text;

  CustomPopupMenuItem({super.key, required this.value, required this.text})
      : super(
          value: value,
          child: Text(text),
        );
}

Future<dynamic> fetchData(String tableName) {
  List<String> fields = ['id', 'name', '__last_update'];
  if (tableName == 'res.partner') {
    fields = ['id', 'name', 'email', '__last_update', 'image_128'];
  } else if (tableName == 'product.template') {
    fields = ['id', 'name'];
  }

  return orpc.callKw({
    'model': tableName,
    'method': 'search_read',
    'args': [],
    'kwargs': {
      'context': {'bin_size': true},
      'domain': [],
      'fields': fields,
      'limit': 80,
    },
  });
}
