import React, { Component } from 'react'
import "./offerProduct.css"
import ProductCart from '../productCart/productCart'
import productimage from "../../../assets/picture/product.png"


export default class OfferProduct extends Component {
    constructor(props) {
        super(props)

        this.state = {
            products: [
                {
                    id: 1,
                    perfumName: "svage elexir",
                    price: "4,500,000",
                    ProductImage: productimage,
                    offerPercentage: "25%",
                    priceAfteroff: "4,000,000"
                },
                {
                    id: 2,
                    perfumName: "creed aventus",
                    price: "6,000,000",
                    ProductImage: productimage,
                    offerPercentage: "10%",
                    priceAfteroff: "5,400,000"
                },
                {
                    id: 3,
                    perfumName: "blue chanel",
                    price: "3,650,000",
                    ProductImage: productimage,
                    offerPercentage: "80%",
                    priceAfteroff: "800,000"
                },
                {
                    id: 4,
                    perfumName: "floris",
                    price: "8,200,000",
                    ProductImage: productimage,
                    offerPercentage: "35%",
                    priceAfteroff: "6,500,000"
                },
                {
                    id: 5,
                    perfumName: "almas",
                    price: "7,000,000",
                    ProductImage: productimage,
                    offerPercentage: "40%",
                    priceAfteroff: "4,000,000",
                },
            ]
        }
    }
    render() {
        return (
            <div>
                <h2 className='offertitle'>محصولات تخفیف با بیشترین تخفیف</h2>
                <div className='offerProductCart'>
                    {this.state.products.map(perf =>
                        <ProductCart
                            key={perf.id}
                            {...perf}
                        />
                    )}
                    <p>{this.state.offerPercentage}</p>
                    <p>{this.state.priceAfteroff}</p>
                </div>
            </div>
        )
    }
}
