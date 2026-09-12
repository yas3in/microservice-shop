import React, { Component } from 'react'
import './header.css'
import Navbar from './navbar/navbar'
import headerMobileIMG from "../../assets/picture/mobile-header.png"

export default class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isMobile: window.innerWidth <= 900
    };
  }

  componentDidMount() {
    window.addEventListener("resize", this.handleResize);
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.handleResize);
  }

  handleResize = () => {
    this.setState({
      isMobile: window.innerWidth <= 900
    });
  };
  render() {
    return (
      <>
        {this.state.isMobile ? (
          // mobile
          <>
            <div className='mobile-header'>
              <div className="navbar-logo-mobile">
                <div className="logo-icon">
                  ✽
                </div>

                <div className="logo-text">
                  <span>Aura</span>
                  <span>Étoile</span>
                </div>
              </div>
              <img src={headerMobileIMG} alt="" />
              <div className='mobile-hwader-content'>
                <span className='mobile-header-span'>مجموعه سلطنتی فرانسه و شرق</span>
                <h1 className='mobile-header-title'>
                  عطرهای اصل و خاص
                  <br />
                  تجلی شکوه و اصالت
                </h1>
                <p className='mobile-header-text'>
                  کشف رایحه‌های ناب و نفیس که هویت شما را به تصویر می‌کشند.
                  با نوآر اسنس، امضای بویایی منحصر‌به‌فرد خود را در میان برترین برندهای
                  نیش جهان بیابید.
                </p>
              </div>
              <Navbar></Navbar>
            </div>
          </>
        ) : (

          <div>
            <Navbar></Navbar>
            <div className='header-container container'>
              <div className='header-content'>

                <span>مجموعه سلطنتی فرانسه و شرق</span>

                <h1>
                  عطرهای اصل و خاص
                  <br />
                  تجلی شکوه و اصالت
                </h1>

                <p>
                  کشف رایحه‌های ناب و نفیس که هویت شما را به تصویر می‌کشند.
                  با نوآر اسنس، امضای بویایی منحصر‌به‌فرد خود را در میان برترین برندهای
                  نیش جهان بیابید.
                </p>
                <button className='header-button'>مشاهده کلکسیون </button>
              </div>
            </div>
          </div>

        )}
      </>
    )
  }
}
