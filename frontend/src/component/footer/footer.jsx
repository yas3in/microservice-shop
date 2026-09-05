import React, { Component } from 'react'
import "./footer.css"

export default class Footer extends Component {
    render() {
        return (
            <div>
                <div className='footer-container'>
                    <div className='send-email'></div>
                    <div className='accessibility all-footer-item'>
                        <h2 className='footer-h2 accessibility-h2'>دسترسی سریع</h2>
                        <div><a href="">کلکسیون عطر ها</a></div>
                        <div><a href="">هدیه</a></div>
                        <div><a href="">سوالات متداول</a></div>
                        <div><a href="">شرایط و قوانین</a></div>
                        <div><a href="">حریم خصوصی</a></div>
                    </div>
                    <div className='service all-footer-item'>
                        <h2 className='footer-h2'>خدمات مشتریان</h2>
                        <div><a href="">تماس با ما</a></div>
                        <div><a href="">پیگیری سفارش</a></div>
                        <div><a href="">بازگشت کالا</a></div>
                        <div><a href="">راهنمای خرید</a></div>
                    </div>
                    <div className='call-info all-footer-item'>
                        <h2 className='footer-h2'>اطلاعات نماس</h2>
                        <div className='call'> +98 939 - 118 - 0646</div>
                        <div className='email'>mojib0646yousefi@gmail.com</div>
                        <div className='location'>بندرعباس هرمزگان</div>
                    </div>
                    <div className='name-logo-bar'>
                        <div className="footer-logo-icon">
                            <p className='logo'>✽</p>
                            <span>Aura</span>
                            <span>Étoile</span>
                        </div>

                        <div className="footer-logo-text">
                            <p>تجربه لوکس ترین عطر ها</p>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
