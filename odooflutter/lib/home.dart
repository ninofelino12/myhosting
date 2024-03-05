import 'package:flutter/material.dart';
import 'package:odooflutter/main.dart';
import 'package:odooflutter/models/model.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final List<Map<String, String>> menuItems = [
    {'value': 'res.partner', 'text': 'Partner'},
    {'value': 'product.template', 'text': 'Product Template'},
    {'value': 'product.category', 'text': 'Product Category'},
    {'value': 'product.product', 'text': 'Product'},
    {'value': 'ir.module.categoryp', 'text': 'Addons Category'},
    {'value': 'ir.module.module', 'text': 'Addons'},
    {'value': 'ir.actions.report', 'text': 'Report'}
  ];
  String _selectedTable = 'product.product'; // Default selected table

  Widget buildListItem(Map<String, dynamic> record) {
    //var unique = record['__last_update'] as String;

    var unique = 'ffghghh65';
    if (record.containsKey('__last_update')) {
      unique = record['__last_update'] as String;
    } else {
      // Handle kasus jika key tidak ditemukan
      unique = 'iouweqwhiouwh8989';
    }

    print(record);
    unique = unique.replaceAll(RegExp(r'[^0-9]'), '');
    final avatarUrl =
        '${orpc.baseURL}/web/image?model=${_selectedTable}&field=avatar_128&id=${record["id"]}&unique=$unique';
    // '${orpc.baseURL}/web/image?model=res.partner&field=image_1920&id=${record["id"]}';

    return ListTile(
      leading: CircleAvatar(backgroundImage: NetworkImage(avatarUrl)),
      title: Text(record['name']),
      subtitle: record['email'] is String ? Text(record['email']) : null,
      // subtitle: Text(record['email'] is String ? record['email'] : ''),
    );
  }

  @override
  Widget build(BuildContext context) {
    var appBar2 = AppBar(
      title: Text('$_selectedTable'),
      actions: <Widget>[
        IconButton(
          icon: const Icon(Icons.search), // Replace with your desired icon
          onPressed: () {
            // Handle search action
            print('Search button pressed!');
          },
        ),
        popBar(),
      ],
    );

    return Scaffold(
      appBar: appBar2,
      body: Center(
        child: FutureBuilder(
          future: fetchData(_selectedTable),
          builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
            if (snapshot.hasData) {
              return ListView.builder(
                itemCount: snapshot.data.length,
                itemBuilder: (context, index) {
                  final record = snapshot.data[index] as Map<String, dynamic>;
                  return buildListItem(record);
                },
              );
            } else {
              if (snapshot.hasError) return Text('Unable to fetch data');
              return CircularProgressIndicator();
            }
          },
        ),
      ),
    );
  }

  PopupMenuButton<String> popBar() {
    var popupMenuButton = PopupMenuButton<String>(
      onSelected: (String result) {
        setState(() {
          print(result);
          _selectedTable = result;
        });
      },
      itemBuilder: (BuildContext context) {
        return [
          const PopupMenuItem<String>(
            value: 'res.partner',
            child: Text('Partner'),
          ),
          const PopupMenuItem<String>(
            value: 'product.template',
            child: Text('Product Template'),
          ),
          const PopupMenuItem<String>(
            value: 'product.category',
            child: Text('Product category'),
          ),
          const PopupMenuItem<String>(
            value: 'product.product',
            child: Text('Product'),
          ),
          const PopupMenuItem<String>(
            value: 'ir.module.category',
            child: Text('Addons Category'),
          ),
          const PopupMenuItem<String>(
            value: 'ir.module.module',
            child: Text('Addons '),
          ),
          const PopupMenuItem<String>(
            value: 'ir.actions.report',
            child: Text('Report'),
          ),
        ];
      },
    );
    return popupMenuButton;
  }
}
