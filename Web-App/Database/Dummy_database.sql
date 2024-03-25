PGDMP         +                |            postgres    15.6 (Debian 15.6-1.pgdg120+2)    15.3 1    F           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            G           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            H           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            I           1262    5    postgres    DATABASE     s   CREATE DATABASE postgres WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE postgres;
                postgres    false            J           0    0    DATABASE postgres    COMMENT     N   COMMENT ON DATABASE postgres IS 'default administrative connection database';
                   postgres    false    3401                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            K           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    16386 	   allergies    TABLE     n   CREATE TABLE public.allergies (
    "allergieID" integer NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.allergies;
       public         heap    postgres    false    4            �            1259    16389    allergies_allergieID_seq    SEQUENCE     �   CREATE SEQUENCE public."allergies_allergieID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."allergies_allergieID_seq";
       public          postgres    false    4    214            L           0    0    allergies_allergieID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."allergies_allergieID_seq" OWNED BY public.allergies."allergieID";
          public          postgres    false    215            �            1259    16393    dishes    TABLE     '  CREATE TABLE public.dishes (
    "dishID" integer NOT NULL,
    name character varying(50) NOT NULL,
    price double precision NOT NULL,
    ingredients character varying[],
    "dietaryCategory" character varying(50) NOT NULL,
    "mealType" character varying(50) NOT NULL,
    image bytea
);
    DROP TABLE public.dishes;
       public         heap    postgres    false    4            �            1259    16398    dishes_dishID_seq    SEQUENCE     �   CREATE SEQUENCE public."dishes_dishID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."dishes_dishID_seq";
       public          postgres    false    216    4            M           0    0    dishes_dishID_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public."dishes_dishID_seq" OWNED BY public.dishes."dishID";
          public          postgres    false    217            �            1259    16399    mealPlan    TABLE     }   CREATE TABLE public."mealPlan" (
    "mealPlanID" integer NOT NULL,
    "dishID" integer NOT NULL,
    date date NOT NULL
);
    DROP TABLE public."mealPlan";
       public         heap    postgres    false    4            �            1259    16402    mealPlan_mealPlanID_seq    SEQUENCE     �   CREATE SEQUENCE public."mealPlan_mealPlanID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public."mealPlan_mealPlanID_seq";
       public          postgres    false    4    218            N           0    0    mealPlan_mealPlanID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."mealPlan_mealPlanID_seq" OWNED BY public."mealPlan"."mealPlanID";
          public          postgres    false    219            �            1259    16403    orders    TABLE     �   CREATE TABLE public.orders (
    "orderID" integer NOT NULL,
    "userID" integer NOT NULL,
    "mealPlanID" integer NOT NULL,
    amount integer NOT NULL,
    "orderDate" date
);
    DROP TABLE public.orders;
       public         heap    postgres    false    4            �            1259    16406    orders_orderID_seq    SEQUENCE     �   CREATE SEQUENCE public."orders_orderID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public."orders_orderID_seq";
       public          postgres    false    220    4            O           0    0    orders_orderID_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public."orders_orderID_seq" OWNED BY public.orders."orderID";
          public          postgres    false    221            �            1259    16407    user_allergy_association    TABLE     `   CREATE TABLE public.user_allergy_association (
    "userId" integer,
    "allergyId" integer
);
 ,   DROP TABLE public.user_allergy_association;
       public         heap    postgres    false    4            �            1259    16410    users    TABLE       CREATE TABLE public.users (
    "userID" integer NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(64) NOT NULL,
    "lastName" character varying(50) NOT NULL,
    "firstName" character varying(50) NOT NULL,
    role character varying(50) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false    4            �            1259    16413    users_userID_seq    SEQUENCE     �   CREATE SEQUENCE public."users_userID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."users_userID_seq";
       public          postgres    false    223    4            P           0    0    users_userID_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."users_userID_seq" OWNED BY public.users."userID";
          public          postgres    false    224            �           2604    16414    allergies allergieID    DEFAULT     �   ALTER TABLE ONLY public.allergies ALTER COLUMN "allergieID" SET DEFAULT nextval('public."allergies_allergieID_seq"'::regclass);
 E   ALTER TABLE public.allergies ALTER COLUMN "allergieID" DROP DEFAULT;
       public          postgres    false    215    214            �           2604    16415    dishes dishID    DEFAULT     r   ALTER TABLE ONLY public.dishes ALTER COLUMN "dishID" SET DEFAULT nextval('public."dishes_dishID_seq"'::regclass);
 >   ALTER TABLE public.dishes ALTER COLUMN "dishID" DROP DEFAULT;
       public          postgres    false    217    216            �           2604    16416    mealPlan mealPlanID    DEFAULT     �   ALTER TABLE ONLY public."mealPlan" ALTER COLUMN "mealPlanID" SET DEFAULT nextval('public."mealPlan_mealPlanID_seq"'::regclass);
 F   ALTER TABLE public."mealPlan" ALTER COLUMN "mealPlanID" DROP DEFAULT;
       public          postgres    false    219    218            �           2604    16417    orders orderID    DEFAULT     t   ALTER TABLE ONLY public.orders ALTER COLUMN "orderID" SET DEFAULT nextval('public."orders_orderID_seq"'::regclass);
 ?   ALTER TABLE public.orders ALTER COLUMN "orderID" DROP DEFAULT;
       public          postgres    false    221    220            �           2604    16418    users userID    DEFAULT     p   ALTER TABLE ONLY public.users ALTER COLUMN "userID" SET DEFAULT nextval('public."users_userID_seq"'::regclass);
 =   ALTER TABLE public.users ALTER COLUMN "userID" DROP DEFAULT;
       public          postgres    false    224    223            9          0    16386 	   allergies 
   TABLE DATA           7   COPY public.allergies ("allergieID", name) FROM stdin;
    public          postgres    false    214   �7       ;          0    16393    dishes 
   TABLE DATA           j   COPY public.dishes ("dishID", name, price, ingredients, "dietaryCategory", "mealType", image) FROM stdin;
    public          postgres    false    216   +8       =          0    16399    mealPlan 
   TABLE DATA           B   COPY public."mealPlan" ("mealPlanID", "dishID", date) FROM stdin;
    public          postgres    false    218   �:       ?          0    16403    orders 
   TABLE DATA           X   COPY public.orders ("orderID", "userID", "mealPlanID", amount, "orderDate") FROM stdin;
    public          postgres    false    220   �:       A          0    16407    user_allergy_association 
   TABLE DATA           I   COPY public.user_allergy_association ("userId", "allergyId") FROM stdin;
    public          postgres    false    222   �:       B          0    16410    users 
   TABLE DATA           Y   COPY public.users ("userID", email, password, "lastName", "firstName", role) FROM stdin;
    public          postgres    false    223   �:       Q           0    0    allergies_allergieID_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."allergies_allergieID_seq"', 1, false);
          public          postgres    false    215            R           0    0    dishes_dishID_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public."dishes_dishID_seq"', 1, false);
          public          postgres    false    217            S           0    0    mealPlan_mealPlanID_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public."mealPlan_mealPlanID_seq"', 1, false);
          public          postgres    false    219            T           0    0    orders_orderID_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public."orders_orderID_seq"', 1, false);
          public          postgres    false    221            U           0    0    users_userID_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."users_userID_seq"', 1, false);
          public          postgres    false    224            �           2606    16421    allergies allergies_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.allergies
    ADD CONSTRAINT allergies_pkey PRIMARY KEY ("allergieID");
 B   ALTER TABLE ONLY public.allergies DROP CONSTRAINT allergies_pkey;
       public            postgres    false    214            �           2606    16423    dishes dishes_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_pkey PRIMARY KEY ("dishID");
 <   ALTER TABLE ONLY public.dishes DROP CONSTRAINT dishes_pkey;
       public            postgres    false    216            �           2606    16425    mealPlan mealPlan_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."mealPlan"
    ADD CONSTRAINT "mealPlan_pkey" PRIMARY KEY ("mealPlanID");
 D   ALTER TABLE ONLY public."mealPlan" DROP CONSTRAINT "mealPlan_pkey";
       public            postgres    false    218            �           2606    16427    orders orders_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY ("orderID");
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    220            �           2606    16429    users users_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("userID");
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    223            �           2606    16440    mealPlan mealPlan_dishID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."mealPlan"
    ADD CONSTRAINT "mealPlan_dishID_fkey" FOREIGN KEY ("dishID") REFERENCES public.dishes("dishID");
 K   ALTER TABLE ONLY public."mealPlan" DROP CONSTRAINT "mealPlan_dishID_fkey";
       public          postgres    false    218    216    3231            �           2606    16445    orders orders_mealPlanID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_mealPlanID_fkey" FOREIGN KEY ("mealPlanID") REFERENCES public."mealPlan"("mealPlanID");
 I   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_mealPlanID_fkey";
       public          postgres    false    3233    218    220            �           2606    16450    orders orders_userID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_userID_fkey" FOREIGN KEY ("userID") REFERENCES public.users("userID");
 E   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_userID_fkey";
       public          postgres    false    223    3237    220            �           2606    16455 @   user_allergy_association user_allergy_association_allergyId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_allergy_association
    ADD CONSTRAINT "user_allergy_association_allergyId_fkey" FOREIGN KEY ("allergyId") REFERENCES public.allergies("allergieID");
 l   ALTER TABLE ONLY public.user_allergy_association DROP CONSTRAINT "user_allergy_association_allergyId_fkey";
       public          postgres    false    222    214    3229            �           2606    16460 =   user_allergy_association user_allergy_association_userId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_allergy_association
    ADD CONSTRAINT "user_allergy_association_userId_fkey" FOREIGN KEY ("userId") REFERENCES public.users("userID");
 i   ALTER TABLE ONLY public.user_allergy_association DROP CONSTRAINT "user_allergy_association_userId_fkey";
       public          postgres    false    223    222    3237            9   ^   x�3�t��2��;���8�˘�-�89�˄�=��$5�ˌӻ���*�L-J�2�N�H�I�K+:�'9�$�˂3�4'-�2��I�.������ Pt      ;   Q  x����N�0E��WD��Q�&u��0�ӂ��b���������Uw�����vF���&���w��Ͳ�'y����,*a�
M� 	��duޚ�n���g�`xѽZ��R<z��I����KPz�wo�̄s(D�B�֢"w�A�x4N�|���B���sl��E���j?D��zt��&�VG{��h����{m���<N�	'W`DWF4��'�^��B饄��x�H�*X�7p�rOx��yk�pc/#�@	�;��f�N����:i���_J�r�D�����^���n]Y׭��'�q��|<"��ҵ�p������&d��+oe[�h�W����g�(!%�/g�v/�4��82���~�!�ј�l�Ş���h����OPI���f��i�*}��A�<a,K&#�K����,3����{]*�z7o��9�1
F��&x8�OG��'	#[�{b0� ��[���W`���	���%��v��I<ɳ�,~
���ԗO3�z�:'����T�W�����E���P������F�/�O�qc�r���=����x~�p�\�(���8D|V���`0��\��      =      x������ � �      ?      x������ � �      A       x�321354004�4�2����ئ\1z\\\ ���      B   �   x���;�0��>L����F��:^��vPH����h(�L1��34���a��h��(�ce�4��O.i�. ȇrkbB4~P�\�Va�^[1��d�JG�ߗ���sm�p��;�97j5�8E�3M���X
;�T�Q\�R)�miW�Z����9[c=�?��;��\^p�     