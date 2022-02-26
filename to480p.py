#!/usr/bin/python3
import json
import os
import subprocess
import getopt
import sys


def generate_preset_json():
    preset_payload = """{
    "PresetList": [
            {
                "AlignAVStart": true,
                "AudioCopyMask": [
                    "copy:aac"
                ],
                "AudioEncoderFallback": "av_aac",
                "AudioLanguageList": [],
                "AudioList": [
                    {
                        "AudioBitrate": 160,
                        "AudioCompressionLevel": -1.0,
                        "AudioDitherMethod": "auto",
                        "AudioEncoder": "av_aac",
                        "AudioMixdown": "stereo",
                        "AudioNormalizeMixLevel": false,
                        "AudioSamplerate": "auto",
                        "AudioTrackDRCSlider": 0.0,
                        "AudioTrackGainSlider": 0.0,
                        "AudioTrackQuality": 1.0,
                        "AudioTrackQualityEnable": false
                    }
                ],
                "AudioSecondaryEncoderMode": true,
                "AudioTrackSelectionBehavior": "first",
                "ChapterMarkers": true,
                "ChildrenArray": [],
                "Default": true,
                "FileFormat": "av_mp4",
                "Folder": false,
                "FolderOpen": false,
                "InlineParameterSets": false,
                "Mp4HttpOptimize": true,
                "Mp4iPodCompatible": false,
                "PictureAutoCrop": true,
                "PictureBottomCrop": 0,
                "PictureChromaSmoothCustom": "",
                "PictureChromaSmoothPreset": "off",
                "PictureChromaSmoothTune": "none",
                "PictureCombDetectCustom": "",
                "PictureCombDetectPreset": "fast",
                "PictureDARWidth": 0,
                "PictureDeblockCustom": "strength=strong:thresh=20:blocksize=8",
                "PictureDeblockPreset": "off",
                "PictureDeblockTune": "medium",
                "PictureDeinterlaceCustom": "",
                "PictureDeinterlaceFilter": "decomb",
                "PictureDeinterlacePreset": "default",
                "PictureDenoiseCustom": "",
                "PictureDenoiseFilter": "off",
                "PictureDenoisePreset": "",
                "PictureDenoiseTune": "none",
                "PictureDetelecine": "off",
                "PictureDetelecineCustom": "",
                "PictureForceHeight": 0,
                "PictureForceWidth": 0,
                "PictureHeight": 480,
                "PictureItuPAR": false,
                "PictureKeepRatio": true,
                "PictureLeftCrop": 0,
                "PictureLooseCrop": false,
                "PictureModulus": 2,
                "PicturePAR": "auto",
                "PicturePARHeight": 27,
                "PicturePARWidth": 32,
                "PictureRightCrop": 0,
                "PictureRotate": "disable=1",
                "PictureSharpenCustom": "",
                "PictureSharpenFilter": "off",
                "PictureSharpenPreset": "",
                "PictureSharpenTune": "",
                "PictureTopCrop": 0,
                "PictureWidth": 720,
                "PresetDescription": "Small H.264 video (up to 480p30) and AAC stereo audio, in an MP4 container.",
                "PresetName": "TO480P30",
                "SubtitleAddCC": false,
                "SubtitleAddForeignAudioSearch": true,
                "SubtitleAddForeignAudioSubtitle": false,
                "SubtitleBurnBDSub": true,
                "SubtitleBurnBehavior": "foreign",
                "SubtitleBurnDVDSub": true,
                "SubtitleLanguageList": [],
                "SubtitleTrackSelectionBehavior": "none",
                "Type": 1,
                "UsesPictureFilters": true,
                "UsesPictureSettings": 1,
                "VideoAvgBitrate": 1000,
                "VideoColorMatrixCodeOverride": 0,
                "VideoEncoder": "x264",
                "VideoFramerate": "30",
                "VideoFramerateMode": "pfr",
                "VideoGrayScale": false,
                "VideoLevel": "3.1",
                "VideoOptionExtra": "",
                "VideoPreset": "veryfast",
                "VideoProfile": "main",
                "VideoQSVAsyncDepth": 4,
                "VideoQSVDecode": false,
                "VideoQualitySlider": 22.0,
                "VideoQualityType": 2,
                "VideoScaler": "swscale",
                "VideoTune": "",
                "VideoTurboTwoPass": true,
                "VideoTwoPass": true,
                "x264Option": "",
                "x264UseAdvancedOptions": false
            }
        ],
        "VersionMajor": 42,
        "VersionMicro": 0,
        "VersionMinor": 0
    }"""
    with open("preset.json", "w") as file:
        decoder = json.JSONDecoder()
        json.dump(decoder.decode(preset_payload), file)


def delete_file(target_file):
    print(f"deleting {target_file} ...")
    os.remove(target_file)


def convert_to_480(target_file, output_folder):
    generate_preset_json()
    pwd = os.getcwd()
    preset_path = pwd + "/" + "preset.json"
    filename = os.path.basename(target_file)
    destination_path = output_folder + "/" + filename.replace(".mp4", ".m4v")
    process = subprocess.Popen(
        ["HandBrakeCLI", "--preset-import-file", preset_path, "-Z", "TO480P30", "-i", target_file,
         "-o", destination_path])
    exit_code = process.wait()
    if exit_code == 0:
        delete_file(target_file)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:i:o:", ["help", "input=", "output="])
    except getopt.GetoptError:
        print(f"{sys.argv[0]} --input <filename> --output <destination folder>")
        sys.exit(2)

    input_file = ""
    output_folder = ""
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(f"{sys.argv[0]} --input <filename> --output <destination folder>")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_folder = arg
    convert_to_480(input_file, output_folder)


if __name__ == '__main__':
    main(sys.argv[1:])
