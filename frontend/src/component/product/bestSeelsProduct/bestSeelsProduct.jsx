import React, { Component } from 'react'
import ProductCart from '../productCart/productCart'
import './bestSeelsProduct.css'
import productimage from "../../../assets/picture/product.png"

export default class BestSeelsProduct extends Component {
    constructor(props) {
        super(props)
        this.state = {
            products: [
                {
                    id: 1,
                    perfumName: "svage elexir",
                    priceforBSP: "4,500,000",
                    ProductImage: productimage,
                },
                {
                    id: 2,
                    perfumName: "creed aventus",
                    priceforBSP: "6,000,000",
                    ProductImage: productimage,
                },
                {
                    id: 3,
                    perfumName: "blue chanel",
                    priceforBSP: "3,650,000",
                    ProductImage: productimage,
                },
                {
                    id: 4,
                    perfumName: "floris",
                    priceforBSP: "8,200,000",
                    ProductImage: productimage,
                },
                {
                    id: 5,
                    perfumName: "almas",
                    priceforBSP: "7,000,000",
                    ProductImage: productimage,
                },
            ]
        }
    }
    render() {
        return (
            <div>
                <h2 className='bestseals-tltle'> محصولات پرطرفدار</h2>
                <div className='best-seel-product'>
                    {this.state.products.map(perf =>
                        <ProductCart
                            key={perf.id}
                            {...perf}
                        />
                    )}
                </div>
            </div>
        )
    }
}
