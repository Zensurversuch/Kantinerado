PGDMP     '    #                |            postgres    15.6 (Debian 15.6-1.pgdg120+2)    15.3 5    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
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
                   pg_database_owner    false    4            �            1259    16384 	   allergies    TABLE     n   CREATE TABLE public.allergies (
    "allergieID" integer NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.allergies;
       public         heap    postgres    false    4            �            1259    16387    allergies_allergieID_seq    SEQUENCE     �   CREATE SEQUENCE public."allergies_allergieID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public."allergies_allergieID_seq";
       public          postgres    false    4    214            S           0    0    allergies_allergieID_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public."allergies_allergieID_seq" OWNED BY public.allergies."allergieID";
          public          postgres    false    215            �            1259    16424    dish_allergy_association    TABLE     `   CREATE TABLE public.dish_allergy_association (
    "dishId" integer,
    "allergyId" integer
);
 ,   DROP TABLE public.dish_allergy_association;
       public         heap    postgres    false    4            �            1259    16416    dishes    TABLE     '  CREATE TABLE public.dishes (
    "dishID" integer NOT NULL,
    name character varying(50) NOT NULL,
    price double precision NOT NULL,
    ingredients character varying[],
    "dietaryCategory" character varying(50) NOT NULL,
    "mealType" character varying(50) NOT NULL,
    image bytea
);
    DROP TABLE public.dishes;
       public         heap    postgres    false    4            �            1259    16415    dishes_dishID_seq    SEQUENCE     �   CREATE SEQUENCE public."dishes_dishID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public."dishes_dishID_seq";
       public          postgres    false    220    4            T           0    0    dishes_dishID_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public."dishes_dishID_seq" OWNED BY public.dishes."dishID";
          public          postgres    false    219            �            1259    16438    mealPlan    TABLE     }   CREATE TABLE public."mealPlan" (
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
          public          postgres    false    224            �            1259    16388    user_allergy_association    TABLE     `   CREATE TABLE public.user_allergy_association (
    "userId" integer,
    "allergyId" integer
);
 ,   DROP TABLE public.user_allergy_association;
       public         heap    postgres    false    4            �            1259    16391    users    TABLE       CREATE TABLE public.users (
    "userID" integer NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(64) NOT NULL,
    "lastName" character varying(50) NOT NULL,
    "firstName" character varying(50) NOT NULL,
    role character varying(50) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false    4            �            1259    16394    users_userID_seq    SEQUENCE     �   CREATE SEQUENCE public."users_userID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public."users_userID_seq";
       public          postgres    false    217    4            W           0    0    users_userID_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public."users_userID_seq" OWNED BY public.users."userID";
          public          postgres    false    218            �           2604    16395    allergies allergieID    DEFAULT     �   ALTER TABLE ONLY public.allergies ALTER COLUMN "allergieID" SET DEFAULT nextval('public."allergies_allergieID_seq"'::regclass);
 E   ALTER TABLE public.allergies ALTER COLUMN "allergieID" DROP DEFAULT;
       public          postgres    false    215    214            �           2604    16419    dishes dishID    DEFAULT     r   ALTER TABLE ONLY public.dishes ALTER COLUMN "dishID" SET DEFAULT nextval('public."dishes_dishID_seq"'::regclass);
 >   ALTER TABLE public.dishes ALTER COLUMN "dishID" DROP DEFAULT;
       public          postgres    false    220    219    220            �           2604    16441    mealPlan mealPlanID    DEFAULT     �   ALTER TABLE ONLY public."mealPlan" ALTER COLUMN "mealPlanID" SET DEFAULT nextval('public."mealPlan_mealPlanID_seq"'::regclass);
 F   ALTER TABLE public."mealPlan" ALTER COLUMN "mealPlanID" DROP DEFAULT;
       public          postgres    false    223    222    223            �           2604    16453    orders orderID    DEFAULT     t   ALTER TABLE ONLY public.orders ALTER COLUMN "orderID" SET DEFAULT nextval('public."orders_orderID_seq"'::regclass);
 ?   ALTER TABLE public.orders ALTER COLUMN "orderID" DROP DEFAULT;
       public          postgres    false    225    224    225            �           2604    16396    users userID    DEFAULT     p   ALTER TABLE ONLY public.users ALTER COLUMN "userID" SET DEFAULT nextval('public."users_userID_seq"'::regclass);
 =   ALTER TABLE public.users ALTER COLUMN "userID" DROP DEFAULT;
       public          postgres    false    218    217            ?          0    16384 	   allergies 
   TABLE DATA           7   COPY public.allergies ("allergieID", name) FROM stdin;
    public          postgres    false    214   �=       F          0    16424    dish_allergy_association 
   TABLE DATA           I   COPY public.dish_allergy_association ("dishId", "allergyId") FROM stdin;
    public          postgres    false    221   1>       E          0    16416    dishes 
   TABLE DATA           j   COPY public.dishes ("dishID", name, price, ingredients, "dietaryCategory", "mealType", image) FROM stdin;
    public          postgres    false    220   N>       H          0    16438    mealPlan 
   TABLE DATA           B   COPY public."mealPlan" ("mealPlanID", "dishID", date) FROM stdin;
    public          postgres    false    223   k>       J          0    16450    orders 
   TABLE DATA           X   COPY public.orders ("orderID", "userID", "mealPlanID", amount, "orderDate") FROM stdin;
    public          postgres    false    225   �>       A          0    16388    user_allergy_association 
   TABLE DATA           I   COPY public.user_allergy_association ("userId", "allergyId") FROM stdin;
    public          postgres    false    216   �>       B          0    16391    users 
   TABLE DATA           Y   COPY public.users ("userID", email, password, "lastName", "firstName", role) FROM stdin;
    public          postgres    false    217   �>       X           0    0    allergies_allergieID_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public."allergies_allergieID_seq"', 1, false);
          public          postgres    false    215            Y           0    0    dishes_dishID_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public."dishes_dishID_seq"', 1, false);
          public          postgres    false    219            Z           0    0    mealPlan_mealPlanID_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public."mealPlan_mealPlanID_seq"', 1, false);
          public          postgres    false    222            [           0    0    orders_orderID_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public."orders_orderID_seq"', 1, false);
          public          postgres    false    224            \           0    0    users_userID_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public."users_userID_seq"', 1, false);
          public          postgres    false    218            �           2606    16398    allergies allergies_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.allergies
    ADD CONSTRAINT allergies_pkey PRIMARY KEY ("allergieID");
 B   ALTER TABLE ONLY public.allergies DROP CONSTRAINT allergies_pkey;
       public            postgres    false    214            �           2606    16423    dishes dishes_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_pkey PRIMARY KEY ("dishID");
 <   ALTER TABLE ONLY public.dishes DROP CONSTRAINT dishes_pkey;
       public            postgres    false    220            �           2606    16443    mealPlan mealPlan_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public."mealPlan"
    ADD CONSTRAINT "mealPlan_pkey" PRIMARY KEY ("mealPlanID");
 D   ALTER TABLE ONLY public."mealPlan" DROP CONSTRAINT "mealPlan_pkey";
       public            postgres    false    223            �           2606    16455    orders orders_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY ("orderID");
 <   ALTER TABLE ONLY public.orders DROP CONSTRAINT orders_pkey;
       public            postgres    false    225            �           2606    16400    users users_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY ("userID");
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    217            �           2606    16432 @   dish_allergy_association dish_allergy_association_allergyId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dish_allergy_association
    ADD CONSTRAINT "dish_allergy_association_allergyId_fkey" FOREIGN KEY ("allergyId") REFERENCES public.allergies("allergieID");
 l   ALTER TABLE ONLY public.dish_allergy_association DROP CONSTRAINT "dish_allergy_association_allergyId_fkey";
       public          postgres    false    214    221    3233            �           2606    16427 =   dish_allergy_association dish_allergy_association_dishId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.dish_allergy_association
    ADD CONSTRAINT "dish_allergy_association_dishId_fkey" FOREIGN KEY ("dishId") REFERENCES public.dishes("dishID");
 i   ALTER TABLE ONLY public.dish_allergy_association DROP CONSTRAINT "dish_allergy_association_dishId_fkey";
       public          postgres    false    220    221    3237            �           2606    16444    mealPlan mealPlan_dishID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public."mealPlan"
    ADD CONSTRAINT "mealPlan_dishID_fkey" FOREIGN KEY ("dishID") REFERENCES public.dishes("dishID");
 K   ALTER TABLE ONLY public."mealPlan" DROP CONSTRAINT "mealPlan_dishID_fkey";
       public          postgres    false    3237    220    223            �           2606    16461    orders orders_mealPlanID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_mealPlanID_fkey" FOREIGN KEY ("mealPlanID") REFERENCES public."mealPlan"("mealPlanID");
 I   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_mealPlanID_fkey";
       public          postgres    false    225    223    3239            �           2606    16456    orders orders_userID_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.orders
    ADD CONSTRAINT "orders_userID_fkey" FOREIGN KEY ("userID") REFERENCES public.users("userID");
 E   ALTER TABLE ONLY public.orders DROP CONSTRAINT "orders_userID_fkey";
       public          postgres    false    225    217    3235            �           2606    16401 @   user_allergy_association user_allergy_association_allergyId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_allergy_association
    ADD CONSTRAINT "user_allergy_association_allergyId_fkey" FOREIGN KEY ("allergyId") REFERENCES public.allergies("allergieID");
 l   ALTER TABLE ONLY public.user_allergy_association DROP CONSTRAINT "user_allergy_association_allergyId_fkey";
       public          postgres    false    3233    214    216            �           2606    16406 =   user_allergy_association user_allergy_association_userId_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_allergy_association
    ADD CONSTRAINT "user_allergy_association_userId_fkey" FOREIGN KEY ("userId") REFERENCES public.users("userID");
 i   ALTER TABLE ONLY public.user_allergy_association DROP CONSTRAINT "user_allergy_association_userId_fkey";
       public          postgres    false    217    3235    216            ?   ^   x�3�t��2��;���8�˘�-�89�˄�=��$5�ˌӻ���*�L-J�2�N�H�I�K+:�'9�$�˂3�4'-�2��I�.������ Pt      F      x������ � �      E      x������ � �      H      x������ � �      J      x������ � �      A       x�321354004�4�2����ئ\1z\\\ ���      B   �   x���;�0��>L����F��:^��vPH����h(�L1��34���a��h��(�ce�4��O.i�. ȇrkbB4~P�\�Va�^[1��d�JG�ߗ���sm�p��;�97j5�8E�3M���X
;�T�Q\�R)�miW�Z����9[c=�?��;��\^p�     