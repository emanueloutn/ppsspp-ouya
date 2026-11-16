param(
 [Parameter(Mandatory=$true)][string]$SourceRoot,
 [Parameter(Mandatory=$true)][string]$NdkRoot,
 [Parameter(Mandatory=$true)][string]$CMakeExe,
 [Parameter(Mandatory=$true)][string]$BuildTools,
 [Parameter(Mandatory=$true)][string]$Jdk,
 [Parameter(Mandatory=$true)][string]$BaseApk,
 [Parameter(Mandatory=$true)][string]$Keystore,
 [Parameter(Mandatory=$true)][string]$KeyAlias
)
$ErrorActionPreference='Stop'
function Assert-Exit([string]$Step) { if ($LASTEXITCODE -ne 0) { throw "$Step failed ($LASTEXITCODE)" } }
$taskRepo=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$taskMeta=Get-Content (Join-Path $taskRepo 'BUILD-INFO.json') -Raw | ConvertFrom-Json
if ((Get-FileHash -LiteralPath $BaseApk -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskMeta.container_base_apk_sha256) { throw 'Base APK SHA256 does not match the documented original' }
if (!$env:OUYA_STORE_PASSWORD -or !$env:OUYA_KEY_PASSWORD) { throw 'Set OUYA_STORE_PASSWORD and OUYA_KEY_PASSWORD for your own signing key' }
$taskBuild=Join-Path $taskRepo 'build'
$taskNative=Join-Path $taskBuild 'native'
New-Item -ItemType Directory -Force $taskNative | Out-Null
$taskVersion='const char *PPSSPP_GIT_VERSION = "v1.17";' + [Environment]::NewLine + '#define PPSSPP_GIT_VERSION_NO_UPDATE 1'
Set-Content -Encoding utf8 -LiteralPath (Join-Path $taskNative 'git-version.cpp') -Value $taskVersion
& $CMakeExe -S $SourceRoot -B $taskNative -G 'MinGW Makefiles' "-DCMAKE_MAKE_PROGRAM=$NdkRoot/prebuilt/windows-x86_64/bin/make.exe" "-DCMAKE_TOOLCHAIN_FILE=$NdkRoot/build/cmake/android.toolchain.cmake" -DANDROID=true -DANDROID_ABI=armeabi-v7a -DANDROID_PLATFORM=android-16 -DANDROID_STL=c++_static -DANDROID_ARM_NEON=TRUE -DCMAKE_BUILD_TYPE=Release -DHEADLESS=OFF -DUNITTEST=OFF -DUSE_DISCORD=OFF
Assert-Exit 'CMake configure'
& $CMakeExe --build $taskNative --target ppsspp_jni --parallel 4
Assert-Exit 'Native build'
$taskClang=Join-Path $NdkRoot 'toolchains/llvm/prebuilt/windows-x86_64/bin'
& "$taskClang/llvm-strip.exe" --strip-unneeded -o "$taskBuild/libppsspp_jni.so" "$taskNative/libppsspp_jni.so"
Assert-Exit 'Strip'
python "$taskRepo/tools/package-ouya.py" --base-apk $BaseApk --native-library "$taskBuild/libppsspp_jni.so" --notice-dir $taskRepo --output "$taskBuild/PPSSPP-OUYA-unsigned.apk"
Assert-Exit 'Package'
& "$BuildTools/zipalign.exe" -f 4 "$taskBuild/PPSSPP-OUYA-unsigned.apk" "$taskBuild/PPSSPP-OUYA-aligned.apk"
Assert-Exit 'Align'
& "$Jdk/bin/java.exe" -jar "$BuildTools/lib/apksigner.jar" sign --ks $Keystore --ks-key-alias $KeyAlias --ks-pass env:OUYA_STORE_PASSWORD --key-pass env:OUYA_KEY_PASSWORD --v1-signing-enabled true --min-sdk-version 16 --out "$taskBuild/PPSSPP-OUYA-signed.apk" "$taskBuild/PPSSPP-OUYA-aligned.apk"
Assert-Exit 'Sign'
& "$Jdk/bin/java.exe" -jar "$BuildTools/lib/apksigner.jar" verify --min-sdk-version 16 "$taskBuild/PPSSPP-OUYA-signed.apk"
Assert-Exit 'Verify'
Get-FileHash "$taskBuild/PPSSPP-OUYA-signed.apk"
