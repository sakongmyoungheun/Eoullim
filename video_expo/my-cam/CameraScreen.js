import { StyleSheet, Text, View, Button, SafeAreaView, TouchableOpacity, Dimensions } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useEffect, useState, useRef } from 'react';
import { Camera } from 'expo-camera';
import { Video } from 'expo-av';
import { shareAsync } from 'expo-sharing';
import * as MediaLibrary from 'expo-media-library';
import axios from 'axios';
import * as FileSystem from 'expo-file-system';
import { styles } from './styles';
const { width } = Dimensions.get('window');
import * as Speech from 'expo-speech';

export default function CameraScreen() {

  const navigation = useNavigation(); // navigation 객체 생성

  let cameraRef = useRef();
  const [hasCameraPermission, setHasCameraPermission] = useState();
  const [hasMicrophonePermission, setHasMicrophonePermission] = useState();
  const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState();
  const [isRecording, setIsRecording] = useState(false);
  const [getAnswer] = useState(false);
  const [video, setVideo] = useState();
  const [showSavedMessage, setShowSavedMessage] = useState(false);
  const [translatedText, setTranslatedText] = useState('');

  useEffect(() => {
    (async () => {
      const cameraPermission = await Camera.requestCameraPermissionsAsync();
      const microphonePermission = await Camera.requestMicrophonePermissionsAsync();
      const mediaLibraryPermission = await MediaLibrary.requestPermissionsAsync();

      setHasCameraPermission(cameraPermission.status === "granted");
      setHasMicrophonePermission(microphonePermission.status === "granted");
      setHasMediaLibraryPermission(mediaLibraryPermission.status === "granted");
    })();
  }, []);

  if (hasCameraPermission === undefined || hasMicrophonePermission === undefined) {
    return <Text>Requestion permissions...</Text>
  } else if (!hasCameraPermission) {
    return <Text>Permission for camera not granted.</Text>
  }

  let recordVideo = () => {
    setIsRecording(true);
    let options = {
      quality: "1080p",
      maxDuration: 60,
      mute: false
    };

    cameraRef.current.recordAsync(options).then((recordedVideo) => {
      setVideo(recordedVideo);
      setIsRecording(false);
    });
  };

  let stopRecording = () => {
    setIsRecording(false);
    cameraRef.current.stopRecording();

    if (video) {
      const getBase64 = async (videoUri) => {
        try {
          console.log(videoUri)
          const fileData = await MediaLibrary.getAssetInfoAsync(videoUri, { mediaType: 'video' });
          return fileData.base64;
        } catch (error) {
          console.error("Error getting base64:", error);
        }
      };

      const uploadFileToServer = async (fileUri) => {
        console.log(fileUri);
        try {
          // 파일을 읽어와서 바이너리 데이터로 변환
          const fileInfo = await FileSystem.getInfoAsync(fileUri);
          if (!fileInfo.exists) {
            throw new Error('File does not exist');
          }
          const fileData = await FileSystem.readAsStringAsync(fileUri, {
            encoding: FileSystem.EncodingType.Base64,
          });

          // FormData에 파일 데이터 추가
          const formData = new FormData();
          formData.append('video', {
            uri: fileUri,
            type: 'video/mp4', // 파일 형식에 따라 변경
            name: 'video.mp4', // 파일 이름에 따라 변경
            data: fileData,
          });

          // 서버로 파일 전송
          const response = await axios.post('http://192.168.9.20:5000/file', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          // setTranslatedText(response.data);
          Speech.speak(response.data);

        } catch (error) {
          console.error('Error uploading file:', error);
          throw error;
        }
      };



      setShowSavedMessage(true);
      setTimeout(() => {
        setShowSavedMessage(false);
      }, 2000);
      MediaLibrary.saveToLibraryAsync(video.uri).then(() => {
        uploadFileToServer(video.uri)
      });
    }
  };

  let goBack = () => {
    navigation.goBack(); // 뒤로가기 버튼 클릭 시 뒤로 이동
  };

  if (video) {
    let shareVideo = () => {
      shareAsync(video.uri).then(() => {
        setVideo(undefined);
      });
    };
  }

  return (
    <Camera style={styles.container} ref={cameraRef} type={'front'}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={isRecording ? stopRecording : recordVideo}>
          <Text style={styles.buttonText}>{isRecording ? "번역하기" : "시작하기"}</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity style={styles.backButton} onPress={goBack}>
        <Text style={styles.backButtonText}>← 뒤로가기</Text>
      </TouchableOpacity>
      {showSavedMessage && (
        <Text style={styles.savedMessage}>저장되었습니다.</Text>
      )}
      <View>
        <Text style={styles.translatedText}>{translatedText}</Text>
      </View>
    </Camera>
  );
}