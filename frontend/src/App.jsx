import React from 'react'
import { Routes, Route } from 'react-router-dom'
import "@fontsource-variable/vazirmatn/wght.css";

import "./App.css"
import Header from './component/header/header'
import ParrentProduct from './component/product/parrentProduct'
import Footer from './component/footer/footer'
import AboutUs from './component/aboutUs/aboutUs'
import ProductDetail from './component/productDetail/productDetail'
import Navbar from './component/header/navbar/navbar'
import ScrollToTop from './scrollToTop'



export default function App() {
  return (
    <>
      <ScrollToTop />
      {/* main page */}
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Header />
              <ParrentProduct />
              <section id="about-us">
                <AboutUs />
              </section>
            </>
          }
        />
        {/* product detail page */}
        <Route
          path="/product/:id"
          element={
            <>
              {/* <Header /> */}
              <Navbar />
              <ProductDetail />
            </>
          }
        />
      </Routes>

      <Footer />
    </>
  )
}
