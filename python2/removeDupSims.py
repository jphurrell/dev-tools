#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simple script to find and delete duplicate XCode Simulators

import re
import pdb

from subprocess import Popen, PIPE
from subprocess import call
import argparse


def createTestData():
    data = '''
== Devices ==
-- iOS 7.1 --
-- iOS 8.1 --
    iPhone 4s (AA0EF8C2-312F-4887-95B6-E2627C57B0C7) (Shutdown) 
    iPad Retina (95570584-3AF7-4B8B-ACF5-511A8875791F) (Shutdown) 
    iPad Air (AA2ED5FF-F979-4C44-A85F-2A8FBB283390) (Shutdown) 
-- iOS 8.2 --
    iPad 2 (CB1AB8B6-859C-4123-9CD2-67ED9ABA5617) (Shutdown) 
    iPad Retina (F4AED88A-B08B-45E8-98CE-F61ABFC9B377) (Shutdown) 
    iPad Air (05198447-B34E-4035-B11A-C62BEC72F829) (Shutdown) 
-- iOS 8.3 --
    iPad 2 (D35D9BC0-AB00-463C-9415-A3FC0E274C01) (Shutdown) 
    iPad Retina (51DBE3D8-9516-4DAC-B82E-BE1F9908386C) (Shutdown) 
    iPad Air (2897737D-9B42-4C17-9185-92AF21B0A72D) (Shutdown) 
-- iOS 8.4 --
    iPad 2 (EAF23E87-251A-4917-B360-B78B37B2D88A) (Shutdown) 
    iPad Retina (38AF63F7-A4F3-4048-A222-9E98475C391B) (Shutdown) 
    iPad Air (71686829-AA34-460E-96DC-701B09148F17) (Shutdown) 
-- iOS 9.0 --
    iPhone 6s Plus (AA51CC06-7D9B-42A0-A3A0-B24CC5225151) (Shutdown) 
    iPad 2 (C2B1207B-39AE-4E19-9A96-12B88119B8E4) (Shutdown) 
    iPad Retina (1E8DCE8E-4C45-474E-93DC-A0E9E246724A) (Shutdown) 
    iPad Air (D63B24CB-80AD-4F08-BB9F-7863F27BD4C5) (Shutdown) 
    iPad Air 2 (8E292B86-D6F0-44B3-8065-0609DD71E64E) (Shutdown) 
-- iOS 9.1 --
    iPhone 4s (E7574BFC-3F47-414D-8B34-EA74D24FEF81) (Shutdown) 
    iPad Air 2 (3C29DE41-54E4-404A-8CD2-94AF5BA99C40) (Shutdown) 
    iPad Pro (79EFB6E1-A730-492B-B2F6-574457C0A7E6) (Shutdown) 
-- iOS 9.2 --
    iPad Air (3A4F1058-D545-43DA-9A4D-3F8A9B053262) (Shutdown) 
    iPad Air 2 (2169D4D8-7F06-418A-A2AD-F911EDE1D033) (Shutdown) 
    iPad Pro (50B7A4CE-56EA-4F3C-B7E0-F0AEDF819669) (Shutdown) 
-- iOS 9.3 --
    iPad 2 (A586BD1E-A0DC-474F-ABDB-2ABBC6BA9605) (Shutdown) 
    iPad Retina (A5A9200F-00E6-477C-9FCC-357EC0F558D6) (Shutdown) 
    iPad Air (C51426AE-85CE-492F-AAD4-08482C2B193D) (Shutdown) 
    iPad Air 2 (C56FC6F2-2CC8-47B9-8ED9-C8609D99A149) (Shutdown) 
    iPad Pro (BD4BA221-BEF2-4AC6-838A-0BC32977DB94) (Shutdown) 
-- iOS 10.0 --
    iPhone 5 (37AD1823-2768-4B45-B881-3CB2AAFEE233) (Shutdown) 
    iPhone 5s (C43A3A3E-1B58-4F78-BE11-8E7633316823) (Shutdown) 
    iPhone 6 Plus (061E6739-0354-4A7E-B2B4-56A402E4B89B) (Shutdown) 
    iPad Air (C7630A10-F917-4C5F-B752-6CBAE9868157) (Shutdown) 
    iPad Air 2 (46427432-952D-4C8E-8F10-71D09A5777DE) (Shutdown) 
    iPad Pro (9.7 inch) (283853CA-7574-411C-91B6-650F7A607FB8) (Shutdown) 
    iPad Pro (12.9 inch) (B6F78D14-2FC0-4106-8E4B-91F245349D09) (Shutdown) 
-- iOS 10.1 --
    iPhone 5 (354FED7A-51E5-45D5-AE50-E82F9EF5324C) (Shutdown) 
    iPad Air 2 (68D1D743-0DCC-4D7E-82FA-8317BBBDE789) (Shutdown) 
    iPad Pro (9.7 inch) (DD8E29A2-2AFC-4BCA-86E4-47447C65E1F0) (Shutdown) 
    iPad Pro (12.9 inch) (11F990F7-2585-4532-8E19-DA4A5DE3A3E1) (Shutdown) 
-- iOS 10.2 --
-- iOS 10.3 --
    iPhone 5 (512671C0-C97C-4A66-8E1F-74FA132EC4D4) (Shutdown) 
    iPhone 5s (2E72B324-842A-45A6-BA6C-C3C248C414AC) (Shutdown) 
    iPad Air 2 (FB1FD2C9-D228-4B66-866D-60F26933016E) (Shutdown) 
    iPad Pro (9.7 inch) (671B59B1-7D90-4E7C-9D5E-FAD3FD607FC1) (Shutdown) 
    iPad Pro (12.9 inch) (9FF4EF3C-0513-464F-995C-F9D07B20B66F) (Shutdown) 
    iPad (5th generation) (71CA2F39-EE59-4AF6-8E98-44823C009F2A) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (498DBD02-7529-4DBD-94EC-A511383F7766) (Shutdown) 
    iPad Pro (10.5-inch) (F6AD20E6-B70D-4EE4-B4AB-42CA9035F4D4) (Shutdown) 
-- iOS 11.0 --
    iPhone 5s (7F117FBD-FA5D-49FE-9FFF-9436BA47FE77) (Shutdown) 
    iPhone 6 Plus (64797E05-9D0C-4163-8C67-D2BB95EFA1E7) (Shutdown) 
    iPhone 6 (D9BDDA69-08F3-43A9-B64B-C7B3B0B79E8E) (Shutdown) 
    iPhone 6s (5BFC074E-2A70-4665-A7AA-0F4BB87B309E) (Shutdown) 
    iPhone 6s Plus (DE67C4CF-E7BB-4344-9BFB-E2D7A9CCADF9) (Shutdown) 
    iPhone SE (51B775A3-C817-46EE-AD01-E845BC3B4376) (Shutdown) 
    iPhone 7 (8309E8F8-0AE9-4A01-B572-2EF21D5FA97F) (Shutdown) 
    iPhone 7 Plus (D3349A77-91BD-40E3-AB2A-776C30E76A6D) (Shutdown) 
    iPad (5th generation) (35D51B56-208B-4A35-BD1F-7897A40704F2) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (73AA4A65-7DCA-4E3C-A801-74F9125E35A7) (Shutdown) 
    iPad Pro (10.5-inch) (DCEE1CB2-60D2-4211-9D9B-46CA3BB124D5) (Shutdown) 
-- iOS 11.1 --
    iPhone 5s (53EDEF0A-5147-4BAC-847C-548A4B08E76F) (Shutdown) 
    iPhone 6 Plus (BE453999-1A8E-45A8-BC8D-EA9BAD7A6F2B) (Shutdown) 
    iPhone 6 (92114B12-5E75-443D-9920-7458F05B41A1) (Shutdown) 
    iPhone 6s (ACED9BBB-322B-4E3A-AFA4-ECFC2880F35B) (Shutdown) 
    iPhone 6s Plus (2B2C8A7E-DA7E-4057-AF29-AA4A54653A2E) (Shutdown) 
    iPad Air (C8DD851D-ED16-483E-B9A4-3F5C053EFAC8) (Shutdown) 
    iPad Air 2 (82117AE3-2ADE-4099-A807-AA00EDB3DAC6) (Shutdown) 
    iPad Pro (9.7-inch) (7C84F46C-7540-4934-A058-584B5D010EF7) (Shutdown) 
    iPad Pro (12.9-inch) (36AE510A-5C38-472B-9C9C-FEF46772EB2F) (Shutdown) 
    iPad (5th generation) (3708C5B3-9099-42E6-859F-5DBF9C778018) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (67F4ADF4-D498-4A2A-A756-C91140389CEA) (Shutdown) 
    iPad Pro (10.5-inch) (51C47828-C0B7-4319-B634-CA4F63F73FA6) (Shutdown) 
-- iOS 11.3 --
    iPhone 5s (51EFE634-0500-46FD-ADEA-E0A9D51882B6) (Shutdown) 
    iPhone 6 Plus (9AFC2213-FAF8-4ABB-B070-A0316CC0D1B0) (Shutdown) 
    iPhone 6 (0DC5C2ED-9A2B-4B8F-BB5D-4FAAF6936ED5) (Shutdown) 
    iPhone 6s (D6D08438-30DE-40C8-9070-8AF1A643486F) (Shutdown) 
    iPad Air 2 (598E0502-90C2-46D9-89A8-B092B5E873AF) (Shutdown) 
    iPad Pro (9.7-inch) (3748E269-B2FF-4948-A43D-4505776BCC9D) (Shutdown) 
    iPad Pro (12.9-inch) (B297F8CC-FFA3-4956-B76F-99EDD168006A) (Shutdown) 
    iPad (5th generation) (36FA5506-CD9E-4479-88A9-EE12314A363E) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (32AC2FDD-BD4E-4F26-900E-01166E1F3B18) (Shutdown) 
    iPad Pro (10.5-inch) (637B5390-3987-4978-8A05-53236BDEC9A0) (Shutdown) 
-- iOS 11.4 --
    iPhone 5s (6631B036-9295-4E64-969B-F5B291968A4B) (Shutdown) 
    iPhone 6 Plus (E9A2D7BF-FE53-4929-8B20-5DC3927171A8) (Shutdown) 
    iPhone 6 (FB1FF649-C1EB-4B9F-9D42-17F1282923FD) (Shutdown) 
    iPhone 6s (5E33E40D-CE07-43EF-8F18-2B26A8121FC9) (Shutdown) 
    iPhone 6s Plus (47194BE7-2935-4DE9-8584-324E44F8A2CA) (Shutdown) 
    iPhone SE (2BAC855C-E3FF-46D1-B013-299DAA2A4F2E) (Shutdown) 
    iPhone 7 (A43282A4-F962-49DF-A525-4AB8AB250D7B) (Shutdown) 
    iPad Pro (9.7-inch) (8D2DFCDF-8879-4BF5-B6B3-193D23BAF284) (Shutdown) 
    iPad Pro (12.9-inch) (637E714D-84B5-426B-8B78-B23C28967AB9) (Shutdown) 
    iPad (5th generation) (E724EB85-01C9-4840-B66D-85CD0A22F7B3) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (A4349BE2-C091-4B68-956F-4813C6ADDF76) (Shutdown) 
    iPad Pro (10.5-inch) (9EF0AB61-778A-4125-941C-BAF30B4EC914) (Shutdown) 
-- iOS 12.1 --
    iPhone 5s (E20FE5B0-BB67-4D1F-B149-7F8E3A88EE6D) (Shutdown) 
    iPhone 6 Plus (32F26733-759D-44FF-B6D1-67052293E0F6) (Shutdown) 
    iPhone 6 (8667EEDD-3664-4652-9CDD-5C822DAFC48E) (Shutdown) 
    iPhone 6s (82CDAF4E-CCED-4912-8B16-1D0E241754CB) (Shutdown) 
    iPhone 6s Plus (22168B25-EDD7-46EB-BFF7-773BDE4E3B71) (Shutdown) 
    iPhone SE (A43EB413-4AD1-48ED-9A66-1A6215264F20) (Shutdown) 
    iPad Pro (12.9-inch) (611DA3E7-4077-41C3-89C3-DB98E05F137E) (Shutdown) 
    iPad (5th generation) (1E2E144E-3272-4342-9EE0-4A31D5979ACA) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (DCABE5F0-21D5-4171-B9F8-53BBB629F2A6) (Shutdown) 
    iPad Pro (10.5-inch) (E93178B6-AC7B-4665-983E-B0FE1EC9D25C) (Shutdown) 
    iPad (6th generation) (68BA22AF-41EF-493E-9F32-F608A369787C) (Shutdown) 
    iPad Pro (11-inch) (833BED79-934A-4A87-942E-A60E4665E468) (Shutdown) 
    iPad Pro (12.9-inch) (3rd generation) (AFB556C0-15FC-4447-B7E4-141059B9BC70) (Shutdown) 
-- iOS 12.2 --
    iPhone 5s (A4CD2750-0C2C-4C0C-8B82-4B92CFBCD89D) (Shutdown) 
    iPhone 6 Plus (FA4F73BC-53B3-4FAD-93B6-F0BE3B40FFA2) (Shutdown) 
    iPhone 6 (FA9F60DE-19BE-4784-877E-CF7EB493769C) (Shutdown) 
    iPhone 6s (AE5199EF-9ECA-460A-931D-FEA88F2B0BC5) (Shutdown) 
    iPhone 6s Plus (8E73124A-7E1C-4B3D-8299-DA5BFEFA62A0) (Shutdown) 
    iPhone SE (2A693029-3A68-421B-A361-C23CDEF4378A) (Shutdown) 
    iPhone 7 (A8E6AA2A-8237-4CEE-A129-58E9B3211CB8) (Shutdown) 
    iPhone 7 Plus (D0B3611A-B5CD-47A8-A9D4-7C58D9CDD53C) (Shutdown) 
    iPhone 8 (DFA44F38-B618-4967-9E6C-7F116CCD80AD) (Shutdown) 
    iPhone 8 Plus (3B518D1A-2879-4FCB-93D6-DF979D2A4E76) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (30405E19-E6DD-488E-9BCD-27CF33B633C8) (Shutdown) 
    iPad Pro (10.5-inch) (2A5EE2D4-42DE-432B-B1D9-A8410915FEAC) (Shutdown) 
    iPad (6th generation) (43575589-41EC-467C-A784-8BA313F1EDB9) (Shutdown) 
    iPad Pro (11-inch) (670B05D1-F977-465B-A1DF-8C733A64B943) (Shutdown) 
    iPad Pro (12.9-inch) (3rd generation) (331C61D6-15B9-4A14-B3F3-1821C555EA9F) (Shutdown) 
    iPad Air (3rd generation) (F645345E-E8EB-4786-A7D4-5C621E82008C) (Shutdown) 
-- iOS 12.4 --
    iPhone 5s (76FD6C19-134C-46B4-B035-29F24DF3A6FC) (Shutdown) 
    iPhone 6 Plus (312912D3-426B-4427-808B-8EDCB30D1589) (Shutdown) 
    iPhone 6 (DB6DA2B6-8CF0-44B1-91D0-A993508FA48B) (Shutdown) 
    iPhone 6s (6E2F652F-0B49-4198-9707-14FB355CB9AE) (Shutdown) 
    iPhone Xs Max (18580064-A8BD-45A3-802C-BDBB58D82B43) (Shutdown) 
    iPhone Xʀ (D72C99C1-EA05-4B58-927B-ABD50EE88FC7) (Shutdown) 
    iPad Air (9A044DE5-A285-4D39-9F74-CFEDCDF581B5) (Shutdown) 
    iPad Air 2 (66D19D5F-3B89-452B-AA76-87BB40332703) (Shutdown) 
    iPad Pro (9.7-inch) (F0E57F43-3370-4BF0-8DE8-1924C2D75EFB) (Shutdown) 
    iPad Pro (12.9-inch) (9503D7B4-D292-4FA9-BE6B-FC8C5FBAD68D) (Shutdown) 
    iPad Pro (12.9-inch) (22222222-2222-2222-2222-222222222222) (Shutdown) 
    iPad (5th generation) (BF1294E6-43C1-4BB8-9D36-31F4743F73D8) (Shutdown) 
    iPad Pro (12.9-inch) (2nd generation) (ED29DBFE-22F7-470A-8A8B-11AF903312F1) (Shutdown) 
    iPad Pro (10.5-inch) (F95F3297-C936-4667-B8CD-939CB5A7BB5B) (Shutdown) 
    iPad (6th generation) (E86586CE-671C-4CF9-AE80-46C815E929E0) (Shutdown) 
    iPad Pro (11-inch) (A4393A31-E985-49EC-BC37-7044288778E0) (Shutdown) 
    iPad Pro (12.9-inch) (3rd generation) (38530A2E-BEDD-427B-B9BF-5F8954C74F42) (Shutdown) 
    iPad Air (3rd generation) (AD2926B7-D7BE-4A46-97B6-47F56E8291FD) (Shutdown) 
-- iOS 13.0 --
    iPhone 8 (5F57391C-7A9F-4A34-BAB4-4201D5216B6F) (Shutdown) 
    iPhone 8 (11111111-1111-1111-1111-111111111111) (Shutdown) 
    iPhone 8 Plus (6F485A29-C3FF-466F-B15D-F6ABCF95C29E) (Shutdown) 
    iPhone Xs (6753A54E-9905-4760-A116-AA0D23BE4A53) (Shutdown) 
    iPhone Xs Max (B60E7D8E-6EFD-4A89-A8C6-C9650D2B75F4) (Shutdown) 
    iPhone Xʀ (FA5C9AEA-2160-4D10-923E-C9D0D17AFD16) (Shutdown) 
    iPhone 11 (1B13D651-CBDF-444C-8775-60969E0C73C9) (Shutdown) 
    iPhone 11 Pro (F6113B66-24F4-41C0-B46F-1320A2CE8BF0) (Shutdown) 
    iPhone 11 Pro Max (50A8080C-ABEB-4186-9884-A4AC048B8FDB) (Shutdown) 
    iPad Pro (9.7-inch) (C12E87FE-C4B1-46DC-A7EF-80EC830C2339) (Shutdown) 
    iPad Pro (11-inch) (B0346739-B3C5-4317-B583-8C871C2388DB) (Shutdown) 
    iPad Pro (12.9-inch) (3rd generation) (729A4B02-EA02-4D00-ABB6-790F62DE5094) (Shutdown) 
    iPad Air (3rd generation) (5C07D3E4-9071-4B41-A731-F8D6DF420A98) (Shutdown) 
-- tvOS 9.0 --
    Apple TV 1080p (A888E5F1-B5FF-4449-A091-56408C677840) (Shutdown) 
-- tvOS 9.1 --
    Apple TV 1080p (4C2AC309-B7F4-46A4-AC45-BBE8B7B1FDC0) (Shutdown) 
-- tvOS 9.2 --
    Apple TV 1080p (8C7E4A80-1698-40D8-994D-F8F03F6456DC) (Shutdown) 
-- tvOS 13.0 --
    Apple TV (CE48ABD7-E344-4619-9B66-774A3139DD53) (Shutdown) 
    Apple TV 4K (C28C13FB-1767-473D-8E6D-7DB5D04801C1) (Shutdown) 
    Apple TV 4K (at 1080p) (116AD99D-B169-49CF-981F-421C47BF605C) (Shutdown) 
-- watchOS 2.0 --
    Apple Watch - 38mm (144C630D-47CD-4B59-BDF1-F74A88DAB78E) (Shutdown) 
    Apple Watch - 42mm (1D0D58DE-1E9D-408C-8C32-C18AD2F13901) (Shutdown) 
-- watchOS 2.1 --
    Apple Watch - 38mm (212103E3-EF5A-4FCD-A7BC-7B92352F5A30) (Shutdown) 
    Apple Watch - 42mm (DBC9B1CD-1D84-4D34-8C6E-74141FAACBFA) (Shutdown) 
-- watchOS 2.2 --
    Apple Watch - 38mm (529CE924-0C20-4D4F-8BAE-A86DDF212C3E) (Shutdown) 
    Apple Watch - 42mm (2B8AD790-0248-48E4-92D0-245B5AA6530A) (Shutdown) 
-- watchOS 3.1 --
    Apple Watch - 38mm (996F2AF3-DB9A-458C-B067-3EA72174822A) (Shutdown) 
    Apple Watch - 42mm (3C200DE2-89D4-485F-9111-5F59B254CB68) (Shutdown) 
    Apple Watch Series 2 - 38mm (7B437CCA-2B78-46B3-B8B4-94BB22547EF0) (Shutdown) 
    Apple Watch Series 2 - 42mm (BED91879-E9BC-46E3-B29F-6F75658C38AA) (Shutdown) 
-- watchOS 3.2 --
    Apple Watch - 38mm (02039252-7A63-4DC7-8EC5-24A1DE7C9F3E) (Shutdown) 
    Apple Watch - 42mm (5906BBF3-14B0-46DC-867A-6BA5A03E08C7) (Shutdown) 
    Apple Watch Series 2 - 38mm (F71C0F42-A37E-4BEE-A523-3CF7DDE854C4) (Shutdown) 
    Apple Watch Series 2 - 42mm (3C1B4827-E8EF-4F58-801C-8D7CE51499C4) (Shutdown) 
-- watchOS 4.0 --
    Apple Watch - 38mm (F75D0FEA-41B3-4168-8B61-1FBE7E2A12B1) (Shutdown) 
    Apple Watch - 42mm (EECFD52F-B9CD-4543-8424-26ADEDF91AAD) (Shutdown) 
    Apple Watch Series 2 - 38mm (F53968B1-6383-4A45-8BE0-938C1E92CC38) (Shutdown) 
    Apple Watch Series 2 - 42mm (715B09FD-2379-425F-B18E-2DE8F4F17693) (Shutdown) 
    Apple Watch Series 3 - 38mm (931EE7AD-1DB9-4894-9E6F-3C9A9CE62538) (Shutdown) 
    Apple Watch Series 3 - 42mm (BE76FA85-B286-4E6A-9774-D024E78FD1B8) (Shutdown) 
-- watchOS 4.1 --
    Apple Watch - 38mm (F9674576-09BD-4355-B84F-1CE812C13290) (Shutdown) 
    Apple Watch - 42mm (2E367519-FE32-45AE-93B7-4589119E8349) (Shutdown) 
    Apple Watch Series 2 - 38mm (717948A3-6619-4B1B-8C15-E135F4C43B34) (Shutdown) 
    Apple Watch Series 2 - 42mm (4227874B-EA67-4B7E-8559-341DBD1437B2) (Shutdown) 
    Apple Watch Series 3 - 38mm (62EFE052-64BB-4A67-B90F-CCE6B7D210D7) (Shutdown) 
    Apple Watch Series 3 - 42mm (0D1E90A4-0392-4402-9CFC-A9DF4A52E323) (Shutdown) 
-- watchOS 4.2 --
    Apple Watch - 38mm (4414FB6A-A46E-49F6-88FF-E6566B991B8D) (Shutdown) 
    Apple Watch - 42mm (4A318E18-804A-47B0-B72A-F1350824FE17) (Shutdown) 
    Apple Watch Series 2 - 38mm (47539AF9-E1B2-4343-AB65-A27D0551B3CE) (Shutdown) 
    Apple Watch Series 2 - 42mm (FCCA162A-0044-48F4-8A8E-21DD970B7142) (Shutdown) 
    Apple Watch Series 3 - 38mm (0C154AEC-5649-4555-8A14-547C7E6571CD) (Shutdown) 
    Apple Watch Series 3 - 42mm (E522FC91-9E71-4A51-8B24-88532E923EBB) (Shutdown) 
-- watchOS 5.2 --
    Apple Watch Series 2 - 38mm (A5B5BA49-F590-49B6-85EC-BFB4855EAA0E) (Shutdown) 
    Apple Watch Series 2 - 42mm (9AA77B7B-9EC6-4745-B20B-E5E6F1EF6ED8) (Shutdown) 
    Apple Watch Series 3 - 38mm (8F54EFDC-F8A1-49E9-87E2-E958ABE70002) (Shutdown) 
    Apple Watch Series 3 - 42mm (8A879AAB-6B7E-4FC6-9F62-F95FD3ABA44B) (Shutdown) 
    Apple Watch Series 4 - 40mm (B2D87AC6-A88D-4F2F-BBCC-957483D33DD2) (Shutdown) 
    Apple Watch Series 4 - 44mm (6DF49012-CE7C-46DD-A69F-483C0A0DCEB5) (Shutdown) 
-- watchOS 5.3 --
    Apple Watch Series 2 - 38mm (5BC9B7FA-EC14-4AAC-B065-5D4BACB09CC0) (Shutdown) 
    Apple Watch Series 2 - 42mm (1AAE69D2-C9DC-4E0D-9DCF-19FBEF9589E5) (Shutdown) 
    Apple Watch Series 3 - 38mm (BA35BDD1-95EF-4A47-9AC4-EDE85C2B8152) (Shutdown) 
    Apple Watch Series 3 - 42mm (C8A33B6F-AFD1-4AAE-8760-D2CB9DF426EC) (Shutdown) 
    Apple Watch Series 4 - 40mm (CAFF2354-E434-49D9-950D-EBF90A3121C5) (Shutdown) 
    Apple Watch Series 4 - 44mm (140A60C6-2B68-4CB1-A6B3-4198DA45CC8B) (Shutdown) 
-- watchOS 6.0 --
    Apple Watch Series 2 - 38mm (253F8F84-45C2-463D-8437-E23AF23C55F4) (Shutdown) 
    Apple Watch Series 2 - 42mm (C1CD7F55-3377-4ACB-9476-8D4422102F1F) (Shutdown) 
    Apple Watch Series 3 - 38mm (525E67B4-52F6-43D0-872A-77576E7C01D1) (Shutdown) 
    Apple Watch Series 3 - 42mm (CDA9AF35-78A6-495E-913E-238109C9B732) (Shutdown) 
    Apple Watch Series 4 - 40mm (B16BD524-493F-418F-8F6D-323BDA7C63AF) (Shutdown) 
    Apple Watch Series 4 - 44mm (626D4873-D1F4-459D-9BCD-D1524BC48120) (Shutdown) 
    Apple Watch Series 5 - 40mm (B7ED78DA-5243-4547-A0F2-E52C6B77579C) (Shutdown) 
    Apple Watch Series 5 - 44mm (F21FE417-C0AE-4038-AF53-7477503C38AF) (Shutdown) 
-- Unavailable: com.apple.CoreSimulator.SimRuntime.tvOS-12-1 --
    Apple TV (AAA0C73A-C9B3-4C6D-89C7-FB9E89CC5A15) (Shutdown) (unavailable, runtime profile not found)
    Apple TV 4K (963A35D5-13E8-45D6-ACC6-CED524B7E4C4) (Shutdown) (unavailable, runtime profile not found)
    Apple TV 4K (at 1080p) (A3E5B1AF-D742-4306-AF45-4AD07D6529EF) (Shutdown) (unavailable, runtime profile not found)
-- Unavailable: com.apple.CoreSimulator.SimRuntime.tvOS-12-2 --
    Apple TV (F76BAED9-863E-4F79-9699-9E646B222DAC) (Shutdown) (unavailable, runtime profile not found)
    Apple TV 4K (FB34B87F-38C4-4961-8D5E-01A7A2694659) (Shutdown) (unavailable, runtime profile not found)
    Apple TV 4K (at 1080p) (1A0BD6B8-124C-4F58-BF4F-202E3A036E30) (Shutdown) (unavailable, runtime profile not found)
-- Unavailable: com.apple.CoreSimulator.SimRuntime.tvOS-12-4 --
    Apple TV (7C305FC4-6E96-4A2D-8C67-A05DA40C4265) (Shutdown) (unavailable, runtime profile not found)
    Apple TV 4K (77B90CCC-4FE0-4CD1-A4FE-2D378F5D8628) (Shutdown) (unavailable, runtime profile not found)
    Apple TV 4K (at 1080p) (81912D68-378D-45AE-80C4-8EE1FFAB67E0) (Shutdown) (unavailable, runtime profile not found)
-- Unavailable: com.apple.CoreSimulator.SimRuntime.watchOS-5-1 --
    Apple Watch Series 2 - 38mm (4E1E8385-B40E-4758-82E6-966F0C38DDF0) (Shutdown) (unavailable, runtime profile not found)
    Apple Watch Series 2 - 42mm (9A6CE458-0277-441C-90CD-8761C7B956D1) (Shutdown) (unavailable, runtime profile not found)
    Apple Watch Series 3 - 38mm (ABB22862-8AF3-4611-A83B-A1586E08235A) (Shutdown) (unavailable, runtime profile not found)
    Apple Watch Series 3 - 42mm (E92ECDC6-9442-46B5-B0EC-5FE45212BD42) (Shutdown) (unavailable, runtime profile not found)
    Apple Watch Series 4 - 40mm (8E0A7F12-0F30-42E2-8138-68BAEB2EE403) (Shutdown) (unavailable, runtime profile not found)
    Apple Watch Series 4 - 44mm (95BB61AA-1010-419C-8DA4-B2BEBF59BC51) (Shutdown) (unavailable, runtime profile not found)
'''

    return data
    

def deleteSim(item,msg):
    if args.dryrun:
        dryRunMsg = "Would have been " + msg 
        normalLog(dryRunMsg)
    else:
        normalLog(msg.capitalize())
        call(["xcrun","simctl","delete",item])
        

def normalLog(str):
    print(str)

def errorLog(str):
    print(str)

def verboseLog(str):
    if args.verbose:
        print(str)

class Sim:
    def __init__(self,osver,name,uuid):
        self.osver = osver
        self.name = name
        self.uuid = uuid


class IOSVer:
    def __init__(self, name):
        self.name = name
        self.sims = []

    def addSim(self, sim):
        if sim.osver == self.name:
            self.sims.append(sim)
        else:
            errorLog("simulator: %s is not for this OS: %s" % (sim.name,self.name))

    def findDuplicates(self):
        list = []
        dupes = []
        for sim in self.sims:
            if sim.name in list:
                verboseLog("\tAlready have %s sim for %s" % (self.name,sim.name))
                dupes.append(sim.uuid)
            else:
                list.append(sim.name)
                verboseLog("Keeping sim for %s %s: %s" % (self.name, sim.name, sim.uuid))
        return dupes
        

    def deleteDuplicates(self):
        toDelete = self.findDuplicates()
        cnt = len(toDelete)
        for item in toDelete:
            msg = "deleting redundant %s simulator: %s" % (self.name,item)
            deleteSim(item, msg)     
        return cnt
                
# main
def main(items):
    lines = items.split("\n")
    
    lastOS = None
    osVers = []
    for line in lines:
        result = re.match("--\s+(.*?)\s+--", line)
        if not result: 
            match = re.match("(.*?)\(([A-F0-9\-]+)\).*",line)
            if match:
                name = match.group(1).strip()
                id = match.group(2)
                sim = Sim(lastOS.name,name,id)
                lastOS.addSim(sim)
        else:
            osVer = IOSVer(result.group(1).strip())
            osVers.append(osVer)
            lastOS = osVer
    
    dupCnt = 0
    for osVer in osVers:
        dupCnt += osVer.deleteDuplicates()
    
    if dupCnt > 0:
        if args.dryrun:
            normalLog("Would have cleaned up %s duplicate simulators" % dupCnt)
        else:
            normalLog("Cleaned up %s duplicate simulators" % dupCnt)
    else:
        normalLog("No duplicate simulators found")

if __name__== "__main__":

    parser = argparse.ArgumentParser(description='Delete duplicate Xcode simulators')
    parser.add_argument('-d', '--dryrun', action='store_true', help='Show which simulators would be removed without actually doing it.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    parser.add_argument('-t', '--test', action='store_true', help='Self test')
    args = parser.parse_args()
    

    if not args.test:
        p = Popen(["xcrun","simctl","list","devices"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        main(output)
    else:
        args.dryrun = True
        output = createTestData()
        main(output)
    
