import React, { useState, useEffect } from 'react'
import './productDetail.css'
import ProductCart from '../product/productCart/productCart'

import productimage from "../../assets/picture/product.png"

import { Autoplay } from 'swiper/modules'
import { Swiper, SwiperSlide } from 'swiper/react'
import 'swiper/css'

import { useParams } from 'react-router-dom'

import { BiSupport } from "react-icons/bi";
import { MdOutlineVerifiedUser } from "react-icons/md";
import { LiaShippingFastSolid } from "react-icons/lia";
import { PiKeyReturnLight } from "react-icons/pi";


export default function ProductDetail() {

  const { id } = useParams()

  const [isAddedToCart, setIsAddedToCart] = useState(false)
  const [perfumeQuantity, setPerfumeQuantity] = useState(1)

  const products = [
    {
      id: 1,
      name: "dior svaage",
      brand: "dior",
      price: "4,500,000",
      discount: "20",
      finalPrice: "3,600,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",
      Images: [
        productimage,
        productimage,
        productimage,
      ],
      volume: "100",
      category: "مردانه"
    },

    {
      id: 2,
      name: "creed aventus",
      brand: "creed",
      price: "6,000,000",
      discount: "10",
      finalPrice: "5,400,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",
      Images: [
        productimage,
        productimage,
        productimage,
      ],
      volume: "100",
      category: "مردانه"
    },

    {
      id: 3,
      name: "blue chanel",
      brand: "chanel",
      price: "3,650,000",
      discount: "20",
      finalPrice: "2,920,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",
      Images: [
        productimage,
        productimage,
        productimage,
      ],
      volume: "100",
      category: "مردانه"
    },

    {
      id: 4,
      name: "floris",
      brand: "floris",
      price: "8,200,000",
      discount: "20",
      finalPrice: "6,500,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",
      Images: [
        productimage,
        productimage,
        productimage,
      ],
      volume: "100",
      category: "مردانه"
    },

    {
      id: 5,
      name: "almas",
      brand: "almas",
      price: "7,000,000",
      discount: "20",
      finalPrice: "4,000,000",
      descriotion: "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Vero, in!",
      Images: [
        productimage,
        productimage,
        productimage,
      ],
      volume: "100",
      category: "مردانه"
    }
  ]


  const product = products.find(
    product => product.id === Number(id)
  )


  const [selectedImage, setSelectedImage] = useState(
    product?.Images[0]
  )


  useEffect(() => {
    setSelectedImage(product?.Images[0])
    setIsAddedToCart(false)
    setPerfumeQuantity(1)
  }, [id])


  const onclickHandler = (image) => {
    setSelectedImage(image)
  }


  const plusPerfumeQuantity = () => {
    setPerfumeQuantity(
      prevQuantity => prevQuantity + 1
    )
  }


  const minusPerfumeQuantity = () => {
    setPerfumeQuantity(
      prevQuantity =>
        prevQuantity > 1
          ? prevQuantity - 1
          : 1
    )
  }


  if (!product) {
    return <h2>این محصول پیدا نشد</h2>
  }


  return (
    <>

      <div className="product-detail">

        <div className="product-purchase">

          <div className="more-detail">

            <h4 className="more-detail__title">
              جزئیات بیشتر
            </h4>

            <div className="more-detail__items">

              <div className="product-detail-row">
                <p>{product.brand}</p>
                <p>برند</p>
              </div>

              <div className="product-detail-row">
                <p>{product.category}</p>
                <p>جنسیت</p>
              </div>

              <div className="product-detail-row">
                <p>{product.volume} میلی لیتر</p>
                <p>حجم</p>
              </div>

            </div>

          </div>


          <div
            className={`buttons-section ${isAddedToCart ? "added" : ""}`}
          >

            <div className="quantity-control">

              <button
                className="quantity-control__minus"
                onClick={minusPerfumeQuantity}
              >
                -
              </button>

              <p>{perfumeQuantity}</p>

              <button
                className="quantity-control__plus"
                onClick={plusPerfumeQuantity}
              >
                +
              </button>

            </div>


            <button
              className="add-to-cart-btn"
              onClick={() => setIsAddedToCart(true)}
            >
              <span className="add-to-cart-btn__text">
                افزودن به سبد خرید
              </span>

              <span className="add-to-cart-btn__check">
                ✓
              </span>
            </button>

          </div>

        </div>


        <div className="product-content">

          <h2 className="product-content__name">
            {product.name}
          </h2>

          <p className="product-content__brand">
            ({product.brand})
          </p>

          <p className="product-content__description">
            {product.descriotion}
          </p>

          <div className="product-content__price">

            <p className="product-content__old-price">
              {product.price}
            </p>

            <p className="product-content__final-price">
              {product.finalPrice}
            </p>

          </div>


          <div className="product-features">

            <div className="product-feature">
              <p>پاسخگویی سریع</p>
              <BiSupport className="product-feature__icon" />
            </div>

            <div className="product-feature">
              <p>ضمانت اصالت کالا</p>
              <MdOutlineVerifiedUser className="product-feature__icon" />
            </div>

            <div className="product-feature">
              <p>ارسال به سراسر کشور</p>
              <LiaShippingFastSolid className="product-feature__icon" />
            </div>

            <div className="product-feature">
              <p>بازگشت کالا</p>
              <PiKeyReturnLight className="product-feature__icon" />
            </div>

          </div>

        </div>


        <div className="product-gallery">

          <div className="product-gallery__thumbnails">

            {product.Images.map((image, index) => (

              <div
                className={`product-gallery__thumbnail ${selectedImage === image ? "active" : ""}`}
                key={index}
                onClick={() => onclickHandler(image)}
              >

                <img
                  src={image}
                  alt={product.name}
                />

              </div>

            ))}

          </div>


          <div className="product-gallery__main">

            <img
              src={selectedImage}
              alt={product.name}
            />

          </div>

        </div>

      </div>


      <div className="related-products">

        <div className="related-products__title">

          <h2 className="related-products__heading">
            محصولات مرتبط
          </h2>

          <p>
            عطر هایی با توجه به سلیقه شما
          </p>

        </div>


        <div className="related-products__section">

          <div className="related-products__slider">

            <Swiper
              modules={[Autoplay]}
              slidesPerView={3}
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
                  slidesPerView: 4,
                  spaceBetween: 20
                }
              }}

              autoplay={{
                delay: 2000,
                pauseOnMouseEnter: true,
                disableOnInteraction: false
              }}
            >

              {products.map((product) => (

                <SwiperSlide key={product.id}>

                  <ProductCart
                    id={product.id}
                    perfumName={product.name}
                    ProductImage={product.Images[0]}
                    price={product.price}
                    priceAfteroff={product.finalPrice}
                  />

                </SwiperSlide>

              ))}

            </Swiper>

          </div>

        </div>

      </div>

    </>
  )
}