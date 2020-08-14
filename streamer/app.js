import { UI } from '@hyext/hy-ui'
import React, { Component } from 'react'
import './app.hycss'

import LogPanel from '../common/LogPanel'
import styles from '../common/styles';
const hyExt = global.hyExt;
const { View, Text, Button, ScrollView, Image, BackgroundImage} = UI

class App extends Component {
  constructor () {
    super()
    this.state = {
      recwords1:"",
      reswords1:"",
      recwords2:"",
      reswords2:"",
      recwords3:"",
      reswords3:"",
      button_state: true,
      listenning: false,
      en: true,
      n : 1,
      workstate:"提词状态：关闭",
      sel: 0
    }
   
    this.commonLog = ((...args) => {
      
      this.setState({
        listenning: true
      })
      clearTimeout(this.tId)
      s = JSON.stringify(args[0].data)
      n = s.length
      if(s[n-2]=='n'){
        
        let arg = []
        arg[0] = {}
        arg[0].header = {"content-type":"utf8"}
        arg[0].url = "http://111.230.195.60:8080"
        arg[0].method = "POST"
        arg[0].data = { "foo": JSON.stringify(args[0].data)}
        arg[0].dataType = "json"
        console.log('发送HTTP请求：' + JSON.stringify(arg))
        hyExt.request(arg[0]).then(resp => {
          console.log('发送HTTP请求成功，返回：' + JSON.stringify(resp.data))
          if(JSON.stringify(resp.data).length!=2){
            var rc = JSON.stringify(args[0].data)
            rc =  rc.substring(1,rc.length-3)
            var rs = JSON.stringify(resp.data)
            rs = rs.substring(1,rs.length-1)
            this.setState({
              listenning: false
            })
            if(this.state.n==1){
              this.setState({
                recwords1:rc,
                // recwords1: JSON.stringify(args[0].data),
                reswords1: rs,
                n:2
              })
            }
            else if(this.state.n==2){
              this.setState({
                listenning: false
              })
              this.setState({
                recwords2:rc,
                // recwords2: JSON.stringify(args[0].data),
                reswords2:rs,
                n:3
              })
            }
            else{
              this.setState({
                listenning: false
              })
              this.setState({
                recwords1:rc,
                // recwords3:  JSON.stringify(args[0].data)[0:-2],
                reswords1: rs,
                recwords2:"",
                reswords2:"",
                n:1
              })
            }
            console.log('语音识别：' + JSON.stringify(args[0].data))  
            console.log('返回消息：' + JSON.stringify(resp.data))  
          }
        }).catch(err => {
          console.log('发送HTTP请求失败，错误信息：' + err.message)
        })
      }
      this.tId = setTimeout(() => {
        this.setState({
          listenning: false
        })
        }, 1000)
    }).bind(this)
    ts = 5000
    setTimeout(() => {this.setState({sel: 1})}, ts);

  }

  set_sel(){
    this.setState({sel: 0})
  }
  
  airecognation1(){
    this.setState({
      button_state: false,
    })
    this.setState({
      en: false,
    })
    let args = []
    args[0] = {}
    args[0].hotwords = ["1","2","3"]
    args[0].callback = this.commonLog
    hyExt.reg.onSpeechRecognition(args[0]).then(() => {
      this.setState({
        workstate: "提词状态：已开启",
       
      })
      console.log('监听当前直播间语音识别消息成功')  
    }).catch(err => {
      this.setState({
        workstate: "提词开启失败"
      })
      console.log('监听当前直播间语音识别消息失败，错误信息：' + err.message)
    })
    
  }

  airecognation(){
    this.setState({
      button_state: false,
    })
    let args = []
    args[0] = {}
    args[0].hotwords = ["1","2","3"]
    args[0].callback = this.commonLog
    hyExt.reg.onSpeechRecognition(args[0]).then(() => {
      this.setState({
        workstate: "提词状态：已开启",
       
      })
      console.log('监听当前直播间语音识别消息成功')  
    }).catch(err => {
      this.setState({
        workstate: "提词开启失败"
      })
      console.log('监听当前直播间语音识别消息失败，错误信息：' + err.message)
    })
    
  }
  offairecognation(){
    this.setState({
      button_state: true,
    })
    hyExt.reg.offSpeechRecognition().then(() => {
      this.setState({
        workstate: "提词状态：关闭",
        sel: 1
      })
      console.log('取消监听当前直播间语音识别消息成功')    
    }).catch(err => {
      this.setState({
        workstate: "提词关闭失败"
      })
      console.log('取消监听当前直播间语音识别消息失败，错误信息：' + err.message)
    })
  }
  render () {
    const {recwords1, reswords1, recwords2, reswords2, recwords3, reswords3, workstate, sel, button_state, listenning,en} = this.state;
 
    if(sel==0){
      return (
        <Image className="bk-image" mode ="cover" src={require('../img/sir1.gif')}></Image>
      )
    }
    else if(en==true){
      return (
        <ScrollView className='container' >
        <BackgroundImage className='bkcontainer' src={require('../img/img5.jpg')}>
        <Text className='voice1'>{recwords1}</Text>
        <Text className='bullet_chat1'>{reswords1}</Text>
        <Text className='voice2'>{recwords2}</Text>
        <Text className='bullet_chat2'>{reswords2}</Text>
        <Text className='en'>请点击下方圆形区域按钮，开启小助手！</Text>
        <Button className='buttonON' onPress={() => this.airecognation1()} >
        <BackgroundImage className='local-image' src={require('../img/sir8.jpg')}>
        </BackgroundImage>
        </Button>
        </BackgroundImage>
        </ScrollView>
      )
    }
    else{
      if(listenning==true){
        return (
          <ScrollView className='container'>
          <BackgroundImage className='bkcontainer' src={require('../img/img5.jpg')}>
          <Image className="listen-image" mode ="cover" src={require('../img/sir7.gif')}></Image>
          <Text className='voice1'>{recwords1}</Text>
          <Text className='bullet_chat1'>{reswords1}</Text>
          <Text className='voice2'>{recwords2}</Text>
          <Text className='bullet_chat2'>{reswords2}</Text>
          </BackgroundImage>
          </ScrollView>
        )
      }
      else{
        if(button_state==true){
          return (
            <ScrollView className='container' >
            <BackgroundImage className='bkcontainer' src={require('../img/img5.jpg')}>
            <Text className='voice1'>{recwords1}</Text>
            <Text className='bullet_chat1'>{reswords1}</Text>
            <Text className='voice2'>{recwords2}</Text>
            <Text className='bullet_chat2'>{reswords2}</Text>
            <Button className='buttonON' onPress={() => this.airecognation()} >
            <BackgroundImage className='local-image' src={require('../img/sir8.jpg')}>
            </BackgroundImage>
            </Button>
            </BackgroundImage>
            </ScrollView>
          )
        }
        else{
          return (
            <ScrollView className='container'>
            <BackgroundImage className='bkcontainer' src={require('../img/img5.jpg')}>
            <Text className='voice1'>{recwords1}</Text>
            <Text className='bullet_chat1'>{reswords1}</Text>
            <Text className='voice2'>{recwords2}</Text>
            <Text className='bullet_chat2'>{reswords2}</Text>
            <Button className='buttonON' onPress={() => this.offairecognation()} >
            <BackgroundImage className='local-image' src={require('../img/sir5.gif')}>
            </BackgroundImage>
            </Button>
            </BackgroundImage>
            </ScrollView>
          )
        }
      }
    }
  }
  
}

export default App
