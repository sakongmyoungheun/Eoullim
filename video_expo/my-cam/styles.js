import { Dimensions, StyleSheet } from 'react-native';
const { width } = Dimensions.get('window');


export const styles = StyleSheet.create({
    color:{
        color:'#F4A608'
      },
    center:{
        textAlign:'center'
      },
      container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
      },
      logo: {
        width: 122, // 이미지의 너비
        height: 63, // 이미지의 높이
        resizeMode: 'contain',
        marginBottom: 20,
      },
      buttonContainer: {
        position: 'absolute',
        bottom: 20,
        left: 0,
        right: 0,
        paddingHorizontal: 20,
      },
      button: {
        height: 50,
        backgroundColor: '#F4A608',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
      },
      buttonContainer1: {
        flexDirection: 'row', // 수평 방향으로 정렬
        justifyContent: 'space-around', // 버튼들을 동일한 간격으로 정렬
        marginBottom: 10, // 아래 여백 추가
      },
      button2: {
        flex: 1, // 버튼이 화면의 가로 길이를 차지하도록 함
        height: 50,
        lineHeight:50,
        backgroundColor: '#F4A608',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
        marginHorizontal: 20, // 좌우 여백 추가
        color: '#fff', // 텍스트 색상 변경
        textAlign: 'center', // 텍스트를 가운데로 정렬
      },
      button3: {
        flex: 1, // 버튼이 화면의 가로 길이를 차지하도록 함
        height: 50,
        lineHeight:50,
        backgroundColor: '#333',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
        marginHorizontal: 20, // 좌우 여백 추가
        color: '#fff', // 텍스트 색상 변경
        textAlign: 'center', // 텍스트를 가운데로 정렬
      },
      buttonText: {
        color: 'white',
        fontSize: 16,
        paddingHorizontal: 20,
      },
      backButton:{
        position:'absolute',
        left:20,
        top:50
      },
      backButtonText:{
        color:'#fff'
      },
      textArea:{
        backgroundColor:'#fff',
        position:'absolute',
        bottom:0,
        width:width
      },
      savedMessage:{
        backgroundColor:'#fff7',
        padding:10,
        borderRadius:10
      }

});