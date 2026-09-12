import React, { Component } from 'react'
import "./offerProduct.css"
import ProductCart from '../productCart/productCart'

import productimage from "../../../assets/picture/product.png"

import { Autoplay } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'

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
                    priceAfteroff: "4,000,000"
                },
                {
                    id: 2,
                    perfumName: "creed aventus",
                    price: "6,000,000",
                    ProductImage: productimage,
                    priceAfteroff: "5,400,000"
                },
                {
                    id: 3,
                    perfumName: "blue chanel",
                    price: "3,650,000",
                    ProductImage: productimage,
                    priceAfteroff: "800,000"
                },
                {
                    id: 4,
                    perfumName: "floris",
                    price: "8,200,000",
                    ProductImage: productimage,
                    priceAfteroff: "6,500,000"
                },
                {
                    id: 5,
                    perfumName: "almas",
                    price: "7,000,000",
                    ProductImage: productimage,
                    priceAfteroff: "4,000,000"
                },
                {
                    id: 6,
                    perfumName: "test",
                    price: "1,500,000",
                    ProductImage: productimage,
                    priceAfteroff: "1,000,000"
                }
            ],

            slide: 0
        }
    }

    nextSlide = () => {
        this.setState(prevState => ({
            slide: Math.min(
                prevState.slide + 1,
                this.state.products.length - 4
            )
        }))
    }

    prevSlide = () => {
        this.setState(prevState => ({
            slide: Math.max(
                prevState.slide - 1,
                0
            )
        }))
    }

    render() {
        return (
            <div>

                <div className='offer-title'>

                    <p className='whach-all'><a href="">← مشاهده همه</a></p>

                    <div className='right-txt'>
                        <span>فرصت محدود برای خرید لوکس</span>
                        <h2>محصولات با بیشترین تخفیف</h2>
                    </div>
                </div>
                <div className='offer-product'>
                    <Swiper
                        modules={[Autoplay]}
                        slidesPerView={5}
                        spaceBetween={20}
                        breakpoints={{
                            0: {
                                slidesPerView: 2,
                                spaceBetween: 10,
                            },
                            900: {
                                slidesPerView: 2,
                                spaceBetween: 20
                            },
                            1200: {
                                slidesPerView: 5,
                                spaceBetween: 20
                            }
                        }}
                        autoplay={{
                            delay: 2000,
                            pauseOnMouseEnter: true,
                            disableOnInteraction: false
                        }}
                    >
                        {this.state.products.map(perf =>
                            <SwiperSlide key={perf.id}>
                                <ProductCart
                                    {...perf}
                                />
                            </SwiperSlide>
                        )}
                    </Swiper>
                </div>
            </div>
        )
    }
}