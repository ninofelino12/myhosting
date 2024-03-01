import 'package:flutter/material.dart';
import 'package:odoo_rpc/odoo_rpc.dart';

// final orpc = OdooClient('http://203.194.112.105:16000');
final orpc = OdooClient('http://192.168.163.48:8015');
void main() async {
  await orpc.authenticate('DEMO', 'admin', 'odooadmin');
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _selectedTable = 'product.product'; // Default selected table

  Future<dynamic> fetchData(String tableName) {
    List<String> fields = ['id', 'name', '__last_update'];
    if (tableName == 'res.partner') {
      fields = ['id', 'name', 'email', '__last_update', 'image_128'];
    } else if (tableName == 'product.template') {
      fields = ['id', 'name'];
    }
    print('start debug');
    print(fields);
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

  Widget buildListItem(Map<String, dynamic> record) {
    //var unique = record['__last_update'] as String;

    var unique = 'ffghghh65';
    if (record.containsKey('__last_update')) {
      unique = record['__last_update'] as String;
    } else {
      // Handle kasus jika key tidak ditemukan
      unique = 'iouweqwhiouwh8989';
    }
    ;
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
      title: Text('Contacts'),
      actions: <Widget>[
        newMethod(),
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

  PopupMenuButton<String> newMethod() {
    return PopupMenuButton<String>(
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
  }
}
