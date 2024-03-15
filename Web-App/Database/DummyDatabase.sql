PGDMP     3        
            |            postgres    15.6 (Debian 15.6-1.pgdg120+2)    15.3 5    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            N           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            O           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            P           1262    5    postgres    DATABASE     s   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE postgres;
                postgres    false            Q           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    3408                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            R           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    16389 	   allergies    TABLE     n   CREATE TABLE public.allergies (
    "allergieID" integer NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.allergies;
       public         heap    postgres    false    4            �            1259    16388    allergies_allergieID_seq    SEQUENCE     �   CREATE SEQUENCE public."allergies_allergieID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."allergies_allergieID_seq";
       public          postgres    false    4    215            S           0    0    allergies_allergieID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."allergies_allergieID_seq" OWNED BY public.allergies."allergieID";
          public          postgres    false    214            �            1259    16424    dish_allergy_association    TABLE     `   CREATE TABLE public.dish_allergy_association (
    "dishId" integer,
    "allergyId" integer
);
 ,   DROP TABLE public.dish_allergy_association;
       public         heap    postgres    false    4            �            1259    16396    dishes    TABLE     '  CREATE TABLE public.dishes (
    "dishID" integer NOT NULL,
    name character varying(50) NOT NULL,
    price double precision NOT NULL,
    ingredients character varying[],
    "dietaryCategory" character varying(50) NOT NULL,
    "mealType" character varying(50) NOT NULL,
    image bytea
);
    DROP TABLE public.dishes;
       public         heap    postgres    false    4            �            1259    16395    dishes_dishID_seq    SEQUENCE     �   CREATE SEQUENCE public."dishes_dishID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."dishes_dishID_seq";
       public          postgres    false    217    4            T           0    0    dishes_dishID_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public."dishes_dishID_seq" OWNED BY public.dishes."dishID";
          public          postgres    false    216            �            1259    16438    mealPlan    TABLE     }   CREATE TABLE public."mealPlan" (
    "mealPlanID" integer NOT NULL,
    "dishID" integer NOT NULL,
    date date NOT NULL
);
    DROP TABLE public."mealPlan";
       public         heap    postgres    false    4            �            1259    16437    mealPlan_mealPlanID_seq    SEQUENCE     �   CREATE SEQUENCE public."mealPlan_mealPlanID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public."mealPlan_mealPlanID_seq";
       public          postgres    false    4    223            U           0    0    mealPlan_mealPlanID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."mealPlan_mealPlanID_seq" OWNED BY public."mealPlan"."mealPlanID";
          public          postgres    false    222            �            1259    16450    orders    TABLE     �   CREATE TABLE public.orders (
    "orderID" integer NOT NULL,
    "userID" integer NOT NULL,
    "mealPlanID" integer NOT NULL,
    amount integer NOT NULL,
    "orderDate" date
);
    DROP TABLE public.orders;
       public         heap    postgres    false    4            �            1259    16449    orders_orderID_seq    SEQUENCE     �   CREATE SEQUENCE public."orders_orderID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public."orders_orderID_seq";
       public          postgres    false    225    4            V           0    0    orders_orderID_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public."orders_orderID_seq" OWNED BY public.orders."orderID";
          public          postgres    false    224            �            1259    16411    user_allergy_association    TABLE     `   CREATE TABLE public.user_allergy_association (
    "userId" integer,
    "allergyId" integer
);
 ,   DROP TABLE public.user_allergy_association;
       public         heap    postgres    false    4            �            1259    16405    users    TABLE       CREATE TABLE public.users (
    "userID" integer NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(64) NOT NULL,
    "lastName" character varying(50) NOT NULL,
    "firstName" character varying(50) NOT NULL,
    role character varying(50) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false    4            �            1259    16404    users_userID_seq    SEQUENCE     �   CREATE SEQUENCE public."users_userID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."users_userID_seq";
       public          postgres    false    219    4            W           0    0    users_userID_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."users_userID_seq" OWNED BY public.users."userID";
          public          postgres    false    218            �           2604    16392    allergies allergieID    DEFAULT     �   ALTER TABLE ONLY public.allergies ALTER COLUMN "allergieID" SET DEFAULT nextval('public."allergies_allergieID_seq"'::regclass);
 E   ALTER TABLE public.allergies ALTER COLUMN "allergieID" DROP DEFAULT;
       public          postgres    false    215    214    215            �           2604    16399    dishes dishID    DEFAULT     r   ALTER TABLE ONLY public.dishes ALTER COLUMN "dishID" SET DEFAULT nextval('public."dishes_dishID_seq"'::regclass);
 >   ALTER TABLE public.dishes ALTER COLUMN "dishID" DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    16441    mealPlan mealPlanID    DEFAULT     �   ALTER TABLE ONLY public."mealPlan" ALTER COLUMN "mealPlanID" SET DEFAULT nextval('public."mealPlan_mealPlanID_seq"'::regclass);
 F   ALTER TABLE public."mealPlan" ALTER COLUMN "mealPlanID" DROP DEFAULT;
       public          postgres    false    223    222    223            �           2604    16453    orders orderID    DEFAULT     t   ALTER TABLE ONLY public.orders ALTER COLUMN "orderID" SET DEFAULT nextval('public."orders_orderID_seq"'::regclass);
 ?   ALTER TABLE public.orders ALTER COLUMN "orderID" DROP DEFAULT;
       public          postgres    false    225    224    225            �           2604    16408    users userID    DEFAULT     p   ALTER TABLE ONLY public.users ALTER COLUMN "userID" SET DEFAULT nextval('public."users_userID_seq"'::regclass);
 =   ALTER TABLE public.users ALTER COLUMN "userID" DROP DEFAULT;
       public          postgres    false    219    218    219            @          0    16389 	   allergies 
   TABLE DATA           7   COPY public.allergies ("allergieID", name) FROM stdin;
    public          postgres    false    215   �=       F          0    16424    dish_allergy_association 
   TABLE DATA           I   COPY public.dish_allergy_association ("dishId", "allergyId") FROM stdin;
    public          postgres    false    221   A>       B          0    16396    dishes 
   TABLE DATA           j   COPY public.dishes ("dishID", name, price, ingredients, "dietaryCategory", "mealType", image) FROM stdin;
    public          postgres    false    217   �>       H          0    16438    mealPlan 
   TABLE DATA           B   COPY public."mealPlan" ("mealPlanID", "dishID", date) FROM stdin;
    public          postgres    false    223   lQ       J          0    16450    orders 
   TABLE DATA           X   COPY public.orders ("orderID", "userID", "mealPlanID", amount, "orderDate") FROM stdin;
    public          postgres    false    225   R       E          0    16411    user_allergy_association 
   TABLE DATA           I   COPY public.user_allergy_association ("userId", "allergyId") FROM stdin;
    public          postgres    false    220   !S       D          0    16405    users 
   TABLE DATA           Y   COPY public.users ("userID", email, password, "lastName", "firstName", role) FROM stdin;
    public          postgres    false    219   QS       X           0    0    allergies_allergieID_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."allergies_allergieID_seq"', 1, false);
          public          postgres    false    214            Y           0    0    dishes_dishID_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public."dishes_dishID_seq"', 1, false);
          public          postgres    false    216            Z           0    0    mealPlan_mealPlanID_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public."mealPlan_mealPlanID_seq"', 1, false);
          public          postgres    false    222            [           0    0    orders_orderID_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public."orders_orderID_seq"', 1, false);
          public          postgres    false    224            \           0    0    users_userID_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."users_userID_seq"', 1, false);
          public          postgres    false    218            �           2606    16394    allergies allergies_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.allergies
    ADD CONSTRAINT allergies_pkey PRIMARY KEY ("allergieID");
 B   ALTER TABLE ONLY public.allergies DROP CONSTRAINT allergies_pkey;
       public            postgres    false    215            �           2606    16403    dishes dishes_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_pkey PRIMARY KEY ("dishID");
 <   ALTER TABLE ONLY public.dishes DROP CONSTRAINT dishes_pkey;
       public            postgres    false    217            �           2606    16443    mealPlan mealPlan_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."mealPlan"
    ADD CONSTRAINT "mealPlan_pkey" PRIMARY KEY ("mealPlanID");
 D   ALTER TABLE ONLY public."mealPlan" DROP CONSTRAINT "mealPlan_pkey";
       public            postgres    false    223            �           2606    16455    orders orders_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY ("orderID");
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    225            �           2606    16410    users users_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("userID");
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    219            �           2606    16432 @   dish_allergy_association dish_allergy_association_allergyId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dish_allergy_association
    ADD CONSTRAINT "dish_allergy_association_allergyId_fkey" FOREIGN KEY ("allergyId") REFERENCES public.allergies("allergieID");
 l   ALTER TABLE ONLY public.dish_allergy_association DROP CONSTRAINT "dish_allergy_association_allergyId_fkey";
       public          postgres    false    221    3233    215            �           2606    16427 =   dish_allergy_association dish_allergy_association_dishId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dish_allergy_association
    ADD CONSTRAINT "dish_allergy_association_dishId_fkey" FOREIGN KEY ("dishId") REFERENCES public.dishes("dishID");
 i   ALTER TABLE ONLY public.dish_allergy_association DROP CONSTRAINT "dish_allergy_association_dishId_fkey";
       public          postgres    false    217    3235    221            �           2606    16444    mealPlan mealPlan_dishID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."mealPlan"
    ADD CONSTRAINT "mealPlan_dishID_fkey" FOREIGN KEY ("dishID") REFERENCES public.dishes("dishID");
 K   ALTER TABLE ONLY public."mealPlan" DROP CONSTRAINT "mealPlan_dishID_fkey";
       public          postgres    false    217    223    3235            �           2606    16461    orders orders_mealPlanID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_mealPlanID_fkey" FOREIGN KEY ("mealPlanID") REFERENCES public."mealPlan"("mealPlanID");
 I   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_mealPlanID_fkey";
       public          postgres    false    223    225    3239            �           2606    16456    orders orders_userID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_userID_fkey" FOREIGN KEY ("userID") REFERENCES public.users("userID");
 E   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_userID_fkey";
       public          postgres    false    225    219    3237            �           2606    16419 @   user_allergy_association user_allergy_association_allergyId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_allergy_association
    ADD CONSTRAINT "user_allergy_association_allergyId_fkey" FOREIGN KEY ("allergyId") REFERENCES public.allergies("allergieID");
 l   ALTER TABLE ONLY public.user_allergy_association DROP CONSTRAINT "user_allergy_association_allergyId_fkey";
       public          postgres    false    3233    220    215            �           2606    16414 =   user_allergy_association user_allergy_association_userId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_allergy_association
    ADD CONSTRAINT "user_allergy_association_userId_fkey" FOREIGN KEY ("userId") REFERENCES public.users("userID");
 i   ALTER TABLE ONLY public.user_allergy_association DROP CONSTRAINT "user_allergy_association_userId_fkey";
       public          postgres    false    220    219    3237            @   ^   x�3�t��2��;���8�˘�-�89�˄�=��$5�ˌӻ���*�L-J�2�N�H�I�K+:�'9�$�˂3�4'-�2��I�.������ Pt      F   w   x�M��1Dѳ���,�����e��׫ԙ�Ɏ�bJ���	�b@$��"�D�q&��wփ���~;%Q�Hb���vO���_���%�<�v�;Jw<�o���Y���=V��r������)K      B      x����n�ǵ�׭� ���NM��8v��/oj8%6D�Fw+,�m�Ye���iʲ��$���8�����KJ��T����Q���<��t���ˡ�|���Ro�~|�/�p��^�����鬷_��ʕ�|ԡ��_��Ex|w����<|~�\������������z���g�5�T�s�w�}���ͫ���S}��<����/�n?xw�f]Wv<?>|��<�9^N��p��r����O�/z���쯿����q�]l�I�&����K���t|����~h�7�K�n���}=�~5�.�����7c�V\nR_�>�?|
o9��i셋�|�tg���#n]����G���_����|>>�x��k^~	�����m�c�������{|�xߗ>�d��pȇ7�\��\����RO�8������t�M8�߫��r�//?>f!z�������[I9��''F�_������ˇ����}��?�Û�{�<���ݕ����?��R�ϩ���\��������O�·��o�D��&���Zd��_����K�k��������N/���G���/Ԋ�����������|����s��T����ۯ�镞�ÿ.��J�����3��V��~�֋_����S��z�3dԝ�z��Ͽ���O��h��U��������p~����w~���o'�M}�i��v��x����x����^�A~�ȏ�O��rmG��÷�����D���﮻��E[V��y�O�[e��������^h�qf�Ճu_��#����̓d����'�w׬�zE��n;9�u����r_3J쫹���c�u}���
\���{8՞{e��=㽆ԓ�0��i�����tb��W�mmu;�5���[[*A��R���FS-l;j���h�kK�ɼ�!sI���b�է���Sf���:��#��C��m�i���6u1�(��ؽ�y�(���C��מ��#�Dc���|^z���x�Fq{�e�u�S�l��КL?�/#�e�UC+���)��R_���Z���0��ڞ䤕�`e��6���?-�3*}EG4}X�G���!�I�Hk�\��#��Z�+K�����&S�6(�)�5��Te�J	]���AII&�#��D�Pe�J4�+*c��ϔ<�]X��mS:���۳�T��,g/Ȍe�4CwaҔ��]u�BΣ%�B.�e�Z�;�HPft�*Ŕ������`����
���ME/L�D!�����sp��T���e��(�Yv�<��
6�E�N��eK�N���ʦ"nR*Nd�2��6ښ��E']��`7���kg��|�)���8�P)�,�����S睸�Mi���e�Ie��p]T�NZ"O���� �RH.*U���$�k�?��0��<�Z�L�Λ��;X����|��X|��m���Ɂ4ZH����4E�Jz�
u��ȴ�Xb- dO�r�15�1�q%4qG l�C얧�k��殔�,��|�mu���aB$x�k��Ȋ�[���A�����B��F�*~q�=F�.�կF�R"���n�^�=L�!w�)�TuΑf�¶��=s%������#c�����cֲ� �T������2�'���Dz�����IJgm���Le��Br
 �&>u]E'5ԁ��S�R�t�=�d��&+󘨉�WP�NC�d�&��'<�I�.zzK�}²�y4�>V���4;�OR��TR��zK�-����	�Br��IãA��>�2����6:}��N��!�	�81n)�ȱCG3Ҝ�mO|H��n�8!E_{�����"� ��&Z3�ML�Щq���"pA`�X6�z�>w�m��c{b<3�`auOM2}`	������٢��F���;\������Iu˫�l�ػ�}�f�P� ��<�Ϻvm5�}$���M�dW� ��2��
�{�ԯ ��&�`M�2�Bq׶�*��S����	рI{��<��r�U��Y�����\˦���T�U��}yN����%(X�]Ż9��Q��Uh�P�0�*j$�R�B�K�o����N�P3��i�Nt������x[ǎ�;����(9QjZT�K� ��ޗD�:$��_��7धP�a���T�p�� ��c1�mT@� ��0�.d�/a ��Q�y���+c�&B��b;�ts,噼BZ`6k���a�9�YAC�V�!ںv��8��8S0�Y)"`�d�]�d��~T+��Y@�1�ǳ	��e����K�e��QDR��	��
D���i��U���݆a� DP��n���efl�i��#��L
�I�7���^�6��8�}�Er�М����`�HW�*�e]Oς/p;���Q���c�Ā4�I���@'�F�gyG�ݤWR`�\�!��agTd���P�@�0Y�	�_�AY��
d�4��|I����H�,����2��ko#S��T�톛`�6I�n)8��	u������	D�>�a=:$:�9��N�5���5��(+X�� ���.2�A��D�
�[��D(�C�T�2�faW��XK�>ǀ��u�<5�%�����V��i���k�����N��>��uz�0�"Z�4\r9R �l��H}D�rNb��RA� v�S�3f)f~ {��XM�m�Ɓ�a`7��&#�nHiL�3��"�*zp�΀���ҒL+�R |Ɇ�a�t+����ļ�\|݈Jƙ��h7:�ԓ��`tt-�J���
����4�04��d�۔0:����[�H�m��iD�h��d�����k�=�#��N��-��LX�n�-R~X'J%�0�[��f�+u@�4�%�������g�H��
��Ȉ"� o��L�˺�+�!R;�ɂP~��E��l��yj-���h���D!�&�(>���FGz�N�D$dV-P����:hS�4��:��V@'V�?��� {��%%�&!e�2�P��!�R���	"x������p���>[��1�@�iF�@�1� c�����*��	�~�<T,�}"I ��:��Q���9% ���v������h�2"�I�ʚ�D��#�M�C��ٸ���4A x�m�N���4�r(ub�4�Yq��!�*�o@7�5<OC+D�X-O!T��x2�V/ 乬�L����I�J�C��{��)�ș0R��P��o4�R�mŨ���=Z�+��RE�פ�!�,(S�+Br��e�	��׳���j�����i�wT<� �E��7@oh0��qC��b��#����8��p�i����SR[�6���ݴ����!M0qԗ+Bΐ:���>#S��H�hҜ�E��H�$�Uw�u�Y��ȹ= 35�9v��~� �����������9ry�am8�l�eMp�cj\,�'2� �� �)�Ox��C2*�w�0(R� f�D�%�n�	�*�yqv������0(8�d"ܔr��SJ�Y��m�q� �F�k�ui J��Gk��!��0!�HSs^�v�:�"� �9��j�5���\ZF$��0��xk�c�ģ�Hy��F���GP����h���Aj�8�Zf���5�A/��Aw	�
T�,�$�ÅlP9�� �{�#Z��΀�lg�5��ƫ!�*z������M�"m��P�{��4-��"^G�F:R2�p��T�À�6��нh3�[� P��z�S�}�Tc�`[kr�fܙ���F ���"0�Ֆ���_�0#�p�#x�P�vd�L��,W�vw�M�
(�a�<�L+��O�^[�@,诂��t�}��h���P��/���MKҭH�I�
~��y��=�(*\�Å<����1P|g�����+q�����|�4�P��j��3��0�p��ѪvE�ֳ}S rkϐ���"
��a�T[�Mwہf�"zbiv�����P��*0�cG9Zb�30,N�`*~���-;d+��Fߪ�̶3�bG_('33
�Ql�4T�ש�86
F��;pv�O�B-�l���<tW��AB���T �  ��1��Aa���:�ov x|�e���RR�!V�Y�� =쾩LM8B�;J��0�<Lf#F�)���(V2iJ�mGt
`=ۊ���0&����_C�]D<�du�?D��Cˠ?(]�";���S�;ut���\H�_�hٔ6;N�Q�y	7斺���j׳z;o��Nj���ΙgH�N~V6�Y��m	�%cO�CE ��x��M�Sq�(v΀T���Lߢ�_�΂\�v�6��L1A�d�ا4�8��h��C� 	X$ �W
��"���Q�@�%�=ӄy���b!F1��Gm�q��"#�GdE���ׂ�	�B#�\*:��g�=���+��!�H&�Z��(�0W��R��;TkJc��#W06���*(�V�9"s�cgg���f��}�m�t�����a��c���}��CC�a���Є�ޏ�
��a����M����>A�
�C�`�&hWؽ�hS��_Y�����=��-�s5�����8���hZ�Tђ�>�U�# ` �V�� � �[l
�eg�(�&wNs�-5O��XS6mg�Ÿ�o�~���:�R&���M��6IS5��w?���R�_����3**��/���ڧ������)�w|�������ٳg�G`P0      H   �   x�U�ˍDAC�u�K��؀s���ڽ�l���!��7ϐ���IO|�>�V�M���˳��p�^PG��z&��;��Th��a�%Tǉ,��p�m�Gܲ�Fs��	O�q�^���c�,Fn��ξ��X�H���[�7o�tW�a�E�����~9�      J   �   x�m�Kr�@C��]&�߻����ŘN���~Щ����P��ڲ%J��D�%|�n"[!u��y�AR�nb�S�G�q�z���j�S����j�~��F=!�v����rT��!2�i,5�8ђIe,��ʍ�d%[�����'ք���"�TvZM�0�]?�-��I���=�'�ѫJ�Pz��Sv�Z0uN�|R��'�x��kfT���Y��D����8=��3Y��/@��^-���N�V���?|����C�1      E       x�321354004�4�2����ئ\1z\\\ ���      D   �   x���;�0��>L����F��:^��vPH����h(�L1��34���a��h��(�ce�4��O.i�. ȇrkbB4~P�\�Va�^[1��d�JG�ߗ���sm�p��;�97j5�8E�3M���X
;�T�Q\�R)�miW�Z����9[c=�?��;��\^p�     