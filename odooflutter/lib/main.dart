import 'package:flutter/material.dart';
import 'package:odoo_rpc/odoo_rpc.dart';
import 'package:odooflutter/home.dart';

final orpc = OdooClient('http://203.194.112.105:16000');
//final orpc = OdooClient('http://192.168.163.48:8015');

final Map<String, Widget Function(BuildContext)> routes = {
  '/': (context) => HomePage(),
  '/pengaturan': (context) => HomePage(),
};
void main() async {
  await orpc.authenticate('DEMO', 'admin', 'odooadmin');
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tutorial Route Flutter',
      initialRoute: '/',
      routes: routes,
    );
  }
}
