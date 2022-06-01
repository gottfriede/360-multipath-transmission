import os

snr0_str = '\
SourceWidth          320\n\
SourceHeight         240\n\
\n\
FrameRateIn          24\n\
FrameRateOut         24\n\
\n\
IDRPeriod           48\n\
\n\
\n\
QP                  40\n\
MeQP0               40\n\
MeQP1               40\n\
MeQP2               40\n\
MeQP3               40\n\
MeQP4               40\n\
MeQP5               40\n\
'

snr1_str = '\
SourceWidth          320\n\
SourceHeight         240\n\
\n\
FrameRateIn          24\n\
FrameRateOut         24\n\
\n\
IDRPeriod           48\n\
\n\
InterLayerPred      1\n\
\n\
QP                  30\n\
MeQP0               30\n\
MeQP1               30\n\
MeQP2               30\n\
MeQP3               30\n\
MeQP4               30\n\
MeQP5               30\n\
'

snr2_str = '\
SourceWidth          320\n\
SourceHeight         240\n\
\n\
FrameRateIn          24\n\
FrameRateOut         24\n\
\n\
IDRPeriod           48\n\
\n\
InterLayerPred      1\n\
\n\
QP                  20\n\
MeQP0               20\n\
MeQP1               20\n\
MeQP2               20\n\
MeQP3               20\n\
MeQP4               20\n\
MeQP5               20\n\
'

encode1_str = '\
FrameRate               24.0\n\
FramesToBeEncoded      24\n\
\n\
BaseLayerMode		2\n\
\n\
IntraPeriod            48\n\
GOPSize                 4\n\
\n\
SearchMode		4\n\
SearchRange		32\n\
\n\
FastBiSearch    1\n\
\n\
\n\
NumLayers		1\n\
LayerCfg		test/layer0_snr0.cfg\n\
'

encode2_str = '\
FrameRate               24.0\n\
FramesToBeEncoded      24\n\
\n\
BaseLayerMode		2\n\
\n\
IntraPeriod            48\n\
GOPSize                 4\n\
\n\
SearchMode		4\n\
SearchRange		32\n\
\n\
FastBiSearch    1\n\
\n\
\n\
NumLayers		2\n\
LayerCfg		test/layer0_snr0.cfg\n\
LayerCfg		test/layer0_snr1.cfg\n\
'

encode3_str = '\
FrameRate               24.0\n\
FramesToBeEncoded      24\n\
\n\
BaseLayerMode		2\n\
\n\
IntraPeriod            48\n\
GOPSize                 4\n\
\n\
SearchMode		4\n\
SearchRange		32\n\
\n\
FastBiSearch    1\n\
\n\
\n\
NumLayers		3\n\
LayerCfg		test/layer0_snr0.cfg\n\
LayerCfg		test/layer0_snr1.cfg\n\
LayerCfg		test/layer0_snr2.cfg\n\
'

def gen_layer_cfg(input_yuv_name):
    f = open('static_svc/layer0_snr0.cfg', 'w')
    content = 'InputFile            ' + input_yuv_name + '\n\n' + snr0_str
    f.write(content)
    f.close()

    f = open('static_svc/layer0_snr1.cfg', 'w')
    content = 'InputFile            ' + input_yuv_name + '\n\n' + snr1_str
    f.write(content)
    f.close()

    f = open('static_svc/layer0_snr2.cfg', 'w')
    content = 'InputFile            ' + input_yuv_name + '\n\n' + snr2_str
    f.write(content)
    f.close()

def gen_encode_cfg(output_svc_name):
    f = open('static_svc/encode_L1.cfg', 'w')
    content = 'OutputFile            ' + output_svc_name + '1.svc\n\n' + encode1_str
    f.write(content)
    f.close()

    f = open('static_svc/encode_L2.cfg', 'w')
    content = 'OutputFile            ' + output_svc_name + '2.svc\n\n' + encode2_str
    f.write(content)
    f.close()

    f = open('static_svc/encode_L3.cfg', 'w')
    content = 'OutputFile            ' + output_svc_name + '3.svc\n\n' + encode3_str
    f.write(content)
    f.close()

def encode():
    os.system('H264AVCEncoderLibTestStatic -pf static_svc/encode_L1.cfg')
    os.system('H264AVCEncoderLibTestStatic -pf static_svc/encode_L2.cfg')
    os.system('H264AVCEncoderLibTestStatic -pf static_svc/encode_L3.cfg')

if __name__ == '__main__':
    for seg in range(30):
        for tile_x in range(12):
            for tile_y in range(8):
                input_yuv_name = 'video/seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '.yuv'
                output_svc_name = 'static_svc/seg' + str(seg) + '_tile' + str(tile_x) + '_' + str(tile_y) + '_L'
                gen_layer_cfg(input_yuv_name)
                gen_encode_cfg(output_svc_name)
                encode()
