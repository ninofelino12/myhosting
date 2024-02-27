// product_bloc.dart

import 'package:flutter/foundation.dart';
import 'package:bloc/bloc.dart';
import '../models/product.dart'; // Assuming your product model file

part 'product_bloc.g.dart';

// Events
abstract class ProductEvent extends Equatable {
  const ProductEvent();

  @override
  List<Object> get props => [];
}

class LoadProductData extends ProductEvent {
  final int index; // Index of the selected data set
  const LoadProductData(this.index);
}

// States
abstract class ProductState extends Equatable {
  const ProductState();

  @override
  List<Object> get props => [];
}

class ProductLoading extends ProductState {}

class ProductLoaded extends ProductState {
  final List<Product> products;
  const ProductLoaded(this.products);
}

class ProductError extends ProductState {
  final String message;
  const ProductError(this.message);
}

class ProductBloc extends Bloc<ProductEvent, ProductState> {
  final List<List<Product>> productData; // Store data from each URL

  ProductBloc(this.productData) : super(ProductLoading()) {
    on<LoadProductData>((event, emit) async {
      try {
        emit(ProductLoading());
        final products = productData[event.index];
        emit(ProductLoaded(products));
      } catch (error) {
        emit(ProductError(error.toString()));
      }
    });
  }
}
