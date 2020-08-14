import { UI } from '@hyext/hy-ui'
import React, { Component } from 'react'
import './app.hycss'

import LogPanel from '../common/LogPanel'
const hyExt = global.hyExt;
const { View, Text, Button, ScrollView } = UI

class App extends Component {
  constructor () {
    super()
    this.state = {
      recwords:"",
      reswords:"",
      workstate:"提词状态：关闭"
    }
    this.commonLog = ((...args) => {
      s = JSON.stringify(args[0].data)
      n = s.length
      if(s[n-2]=='n'){
        
        let arg = []
        arg[0] = {}
        arg[0].header = {"content-type":"utf8"}
        arg[0].url = "http://106.53.217.177:8080"
        arg[0].method = "POST"
        arg[0].data = { foo: JSON.stringify(args[0].data)}
        arg[0].dataType = "json"
        console.log('发送HTTP请求：' + JSON.stringify(arg))
        hyExt.request(arg[0]).then(resp => {
          console.log('发送HTTP请求成功，返回：' + JSON.stringify(resp.data))
          if(JSON.stringify(resp.data).length!=2){
            this.setState({
              recwords: '语音识别信息：' + JSON.stringify(args[0].data),
              reswords:'提词信息：' + JSON.stringify(resp.data)
            })
            console.log('语音识别：' + JSON.stringify(args[0].data))  
            console.log('返回消息：' + JSON.stringify(resp.data))  
          }
        }).catch(err => {
          console.log('发送HTTP请求失败，错误信息：' + err.message)
        })
    }
      
    }).bind(this)
  
  }
  airecognation(){
    let args = []
    args[0] = {}
    args[0].hotwords = ["1","2","3"]
    args[0].callback = this.commonLog
    hyExt.reg.onSpeechRecognition(args[0]).then(() => {
      this.setState({
        workstate: "提词状态：已开启"
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
    hyExt.reg.offSpeechRecognition().then(() => {
      this.setState({
        workstate: "提词状态：关闭"
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
    const {recwords, reswords, workstate} = this.state;
    return (
      <View className='bkcontainer'>
        <View className='container'>
          <Text className='wordtitle'>智能提词</Text>
          <View className='section'>
            <Button className='buttonON' onPress={() => this.airecognation()}>开启提词</Button>
          </View>
          <View className='section'>
            <Button className='buttonOFF' onPress={() => this.offairecognation()}>关闭提词</Button>
          </View>
        </View>
        <View className='word'>
          <Text>{workstate}</Text>
        </View>
        <View className='recogtext'>
          <Text className='wordtext'>{recwords}</Text>
        </View>
        <View className='responstext'>
          <Text>{reswords}</Text>
        </View>
      </View>
    )
  }
}

export default App
