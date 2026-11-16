from pathlib import Path
import zipfile, struct, hashlib, json
def remove_ouya_game_category(blob):
 data=bytearray(blob);pos=8;strings=[];result=bytearray(data[:8]);removed=0
 def len8(off):
  a=data[off];off+=1
  if a&128:a=((a&127)<<8)|data[off];off+=1
  return a,off
 def len16(off):
  a=struct.unpack_from('<H',data,off)[0];off+=2
  if a&32768:a=((a&32767)<<16)|struct.unpack_from('<H',data,off)[0];off+=2
  return a,off
 while pos<len(data):
  typ,header,size=struct.unpack_from('<HHI',data,pos)
  assert size>=8
  if typ==1:
   count,style_count,flags,start,style_start=struct.unpack_from('<IIIII',data,pos+8)
   for i in range(count):
    off=pos+start+struct.unpack_from('<I',data,pos+header+4*i)[0]
    if flags&256:
     _,off=len8(off);length,off=len8(off);value=bytes(data[off:off+length]).decode('utf-8')
    else:
     length,off=len16(off);value=bytes(data[off:off+length*2]).decode('utf-16le')
    strings.append(value)
  skip=False
  if typ==0x0102:
   ext=pos+16;name=struct.unpack_from('<I',data,ext+4)[0]
   if strings[name]=='category':
    ast,asz,acount=struct.unpack_from('<HHH',data,ext+8)
    for i in range(acount):
     attr=ext+ast+i*asz
     value=struct.unpack_from('<I',data,attr+16)[0]
     if data[attr+15]==3 and strings[value] in ('tv.ouya.intent.category.GAME','tv.ouya.intent.category.APP'):
      end=pos+size;et,eh,es=struct.unpack_from('<HHI',data,end)
      assert et==0x0103 and struct.unpack_from('<I',data,end+20)[0]==name
      pos=end+es;removed+=1;skip=True;break
  if skip:continue
  result.extend(data[pos:pos+size]);pos+=size
 assert removed==1, f'Expected one OUYA category, found {removed}'
 struct.pack_into('<I',result,4,len(result))
 return bytes(result)

import argparse
parser=argparse.ArgumentParser(description="Package the OUYA native fix with preserved upstream credits")
parser.add_argument('--base-apk',required=True)
parser.add_argument('--native-library',required=True)
parser.add_argument('--output',required=True)
parser.add_argument('--notice-dir',required=True)
args=parser.parse_args()
base=Path(args.base_apk);native=Path(args.native_library)
notices=Path(args.notice_dir)
expected=json.loads((notices/'BUILD-INFO.json').read_text(encoding='utf-8-sig'))['container_base_apk_sha256']
if hashlib.sha256(base.read_bytes()).hexdigest()!=expected:
 raise SystemExit('Base APK SHA256 does not match BUILD-INFO.json')
# Only the exact package string changes. Java/JNI class names remain original.
old='org.ppsspp.ppsspp'; new='org.ppsspp.ouyapp'
assert len(old)==len(new)
with zipfile.ZipFile(base) as zin, zipfile.ZipFile(Path(args.output),'w',zipfile.ZIP_DEFLATED) as zout:
 for item in zin.infolist():
  upper=item.filename.upper()
  if upper.startswith('META-INF/') and (upper=='META-INF/MANIFEST.MF' or upper.endswith(('.RSA','.DSA','.EC','.SF'))): continue
  data=zin.read(item.filename)
  if item.filename=='AndroidManifest.xml':
   n=0
   for enc,prefix in [('utf-8',bytes([len(old),len(old)])),('utf-16le',struct.pack('<H',len(old)))]:
    needle=prefix+old.encode(enc)+(b'\0' if enc=='utf-8' else b'\0\0')
    replacement=prefix+new.encode(enc)+(b'\0' if enc=='utf-8' else b'\0\0')
    n+=data.count(needle);data=data.replace(needle,replacement)
   assert n==1, f'Expected one package string, found {n}'
   # This native build targets Android API 16, matching OUYA Android 4.1.
   data=bytearray(data); pos=8; resource_ids=[]; changed=0
   while pos < len(data):
    chunk_type, header_size, chunk_size=struct.unpack_from('<HHI',data,pos)
    if chunk_type==0x0180:
     resource_ids=list(struct.unpack_from('<'+'I'*((chunk_size-header_size)//4),data,pos+header_size))
    elif chunk_type==0x0102:
     ext=pos+16
     attr_start,attr_size,attr_count=struct.unpack_from('<HHH',data,ext+8)
     for i in range(attr_count):
      attr=ext+attr_start+i*attr_size
      name=struct.unpack_from('<I',data,attr+4)[0]
      if name<len(resource_ids) and resource_ids[name]==0x0101020c:
       assert data[attr+15]==0x10
       struct.pack_into('<I',data,attr+16,16);changed+=1
    assert chunk_size>=8
    pos+=chunk_size
   assert changed==1, 'Expected one minSdkVersion attribute'
   data=remove_ouya_game_category(bytes(data))
  elif item.filename=='resources.arsc':
   # Rename only exact six-character app-name strings, preserving all offsets.
   oldlabel='PPSSPP';newlabel='OUYA17';n=0
   for enc,prefix in [('utf-8',b'\x06\x06'),('utf-16le',b'\x06\x00')]:
    needle=prefix+oldlabel.encode(enc)+(b'\0' if enc=='utf-8' else b'\0\0')
    repl=prefix+newlabel.encode(enc)+(b'\0' if enc=='utf-8' else b'\0\0')
    n+=data.count(needle);data=data.replace(needle,repl)
   assert n>0, 'Could not rename application label'
  elif item.filename=='lib/armeabi-v7a/libppsspp_jni.so':data=native.read_bytes()
  zout.writestr(item,data)
 for name in ('LICENSE.TXT','NOTICE.md','CREDITS.md'):
  zout.write(notices/name,'assets/OUYA/'+name)
print('Packaged native correction as org.ppsspp.ouyapp, label OUYA17')
