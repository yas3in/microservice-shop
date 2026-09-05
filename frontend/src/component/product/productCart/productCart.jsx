import React, { Component } from 'react'
import './productCart.css'

export default class ProductCart extends Component {

    render() {
        return (
            <div className='ProductCart'>

                {/* produuct cart image */}
                <div className='product-image'>
                    <img src={this.props.ProductImage} alt="" />
                </div>

                {/* product cart offer */}
                {this.props.offerPercentage && (
                    <p className='offerPercentage'>{this.props.offerPercentage}</p>
                )}

                {/* product cart name title */}
                <h3 className='perfum-title'>
                    {this.props.perfumName}
                </h3>
                {/* perfum discription */}
                <p className='perfum-discription'>
                    Lorem ipsum dolor, sit amet consectetur adipisicing elit. Reiciendis, quia?
                </p>

                <div className='product-text'>

                    {/* old price */}
                    {this.props.priceforBSP && (
                        <p className='BSPprice'>{this.props.priceforBSP}</p>
                    )}

                    {/* new price */}
                    {this.props.priceAfteroff && (
                        <div className='offerPrice'>
                            <p>{this.props.priceAfteroff}</p>
                            <del className='old-price'>
                                {this.props.price}
                            </del>
                        </div>
                    )}

                </div>
            </div>
        )
    }
}