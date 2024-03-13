// HomeScreen.js
import React from 'react';
import { View, TouchableOpacity, Text, Image } from 'react-native';
import { styles } from './styles';

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Image source={require('./logo.png')} style={styles.logo} />
      <Text>모두를 위한 언어:</Text>
      <Text><Text style={styles.color}>소통</Text>의 장벽을 넘어서</Text>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Camera')}>
          <Text style={styles.buttonText}>시작하기</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
