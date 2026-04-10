# ☁️ AWS CloudFormation Templates

Colección de plantillas de AWS CloudFormation para aprovisionar infraestructura en la nube de forma declarativa e incremental. Los templates cubren desde una instancia EC2 básica hasta configuraciones completas con VPC, IAM, S3 y grupos de seguridad.

---

## 📋 Descripción

Este proyecto es un conjunto de plantillas de **Infrastructure as Code (IaC)** escritas en YAML para AWS CloudFormation. El objetivo es aprender y practicar el aprovisionamiento de recursos AWS de manera reproducible, versionada y automatizada, comenzando con ejemplos simples y aumentando gradualmente la complejidad.

---

## 🛠️ Tecnologías

| Tecnología | Descripción |
|---|---|
| **AWS CloudFormation** | Servicio de IaC nativo de AWS |
| **YAML** | Formato de las plantillas |
| **AWS EC2** | Instancias de cómputo |
| **AWS VPC** | Red virtual privada |
| **AWS IAM** | Gestión de identidad y acceso |
| **AWS S3** | Almacenamiento de objetos |
| **AWS EIP** | IP elástica estática |

---

## 📁 Estructura del Proyecto

```
cloudformation/
├── 01-ec2-basic.yaml                          # EC2 básico (nivel inicial)
├── 02-ec2-security-group-elastic-ip.yaml      # EC2 con Security Groups e IP elástica
├── 03-iam-role-vpc-s3-bucket.yaml             # IAM Role + VPC + S3 Bucket con política
├── 04-iam-user-group-vpc-internet-gateway.yaml # IAM User/Group + S3 + VPC + Internet Gateway
├── 05-iam-admin-group-user-vpc-s3.yaml        # IAM Admin + S3 Bucket + VPC
└── README.md
```

---

## 📄 Detalle de cada Template

### `01-ec2-basic.yaml`
Plantilla mínima. Lanza una instancia EC2 `t2.micro` en `us-east-1a`.
- **Recursos:** `AWS::EC2::Instance`

### `02-ec2-security-group-elastic-ip.yaml`
EC2 con dos Security Groups y una Elastic IP asociada. El `SecurityGroupDescription` se recibe como parámetro.
- **Recursos:** `EC2::Instance`, `EC2::EIP`, `EC2::SecurityGroup` (x2)
- **Parámetros:** `SecurityGroupDescription`, `AdminCidr`
- **Outputs:** IP elástica asignada

### `03-iam-role-vpc-s3-bucket.yaml`
Crea un rol IAM para EC2 con acceso completo a S3, una VPC y un bucket S3 privado.
- **Recursos:** `IAM::Role`, `EC2::VPC`, `S3::Bucket`
- **Parámetros:** `RoleName`, `BucketName` (opcionales)
- **Nota:** si no se envían estos parámetros, CloudFormation genera los nombres automáticamente.

### `04-iam-user-group-vpc-internet-gateway.yaml`
Infraestructura completa con usuario y grupo IAM, bucket S3 privado, VPC e Internet Gateway. Incluye Outputs para todos los recursos.
- **Recursos:** `IAM::User`, `IAM::Group`, `S3::Bucket`, `EC2::VPC`, `EC2::InternetGateway`

### `05-iam-admin-group-user-vpc-s3.yaml`
Grupo IAM con política mínima de laboratorio, usuario admin, membresía al grupo, bucket S3 y VPC.
- **Recursos:** `IAM::Group`, `IAM::User`, `IAM::UserToGroupAddition`, `S3::Bucket`, `EC2::VPC`

---

## ✅ Requisitos Previos

- Cuenta de **AWS** activa
- **AWS CLI** instalado y configurado
  ```bash
  aws configure
  ```
- Permisos IAM suficientes para crear los recursos de cada template (EC2, IAM, S3, VPC)
- _(Opcional)_ Acceso a la consola de **AWS CloudFormation**

### Instalación de AWS CLI

```bash
# macOS
brew install awscli

# Verificar instalación
aws --version
```

---

## ⚙️ Configuración

Configura tus credenciales de AWS antes de desplegar:

```bash
aws configure
# AWS Access Key ID:     <tu-access-key>
# AWS Secret Access Key: <tu-secret-key>
# Default region name:   us-east-1
# Default output format: json
```

Para templates con **parámetros** (ej. `02-ec2-security-group-elastic-ip.yaml` o `03-iam-role-vpc-s3-bucket.yaml`), puedes pasarlos en línea o mediante un archivo JSON de parámetros.

---

## 🚀 Cómo Desplegar

### Opción 1 — AWS CLI

```bash
# Crear un stack nuevo
aws cloudformation create-stack \
  --stack-name <nombre-del-stack> \
  --template-body file://<nombre-del-archivo>.yaml \
  --capabilities CAPABILITY_NAMED_IAM

# Ejemplo con parámetros
aws cloudformation create-stack \
  --stack-name ec2-sg-eip-stack \
  --template-body file://02-ec2-security-group-elastic-ip.yaml \
  --parameters ParameterKey=SecurityGroupDescription,ParameterValue="Mi grupo de seguridad" \
  --capabilities CAPABILITY_NAMED_IAM

# Ejemplo por defecto en template 03 (AWS genera RoleName y BucketName)
aws cloudformation create-stack \
  --stack-name iam-vpc-s3-stack \
  --template-body file://03-iam-role-vpc-s3-bucket.yaml \
  --capabilities CAPABILITY_NAMED_IAM

# Ejemplo con nombres personalizados para rol y bucket
aws cloudformation create-stack \
  --stack-name iam-vpc-s3-custom-stack \
  --template-body file://03-iam-role-vpc-s3-bucket.yaml \
  --parameters ParameterKey=RoleName,ParameterValue="Cris" ParameterKey=BucketName,ParameterValue="mys3-bucket2023" \
  --capabilities CAPABILITY_NAMED_IAM
```

### Opción 2 — Consola de AWS

1. Ir a **AWS Console → CloudFormation → Create Stack**
2. Seleccionar **"Upload a template file"**
3. Subir el archivo `.yaml` deseado
4. Completar los parámetros requeridos y seguir el asistente

### Actualizar un Stack Existente

```bash
aws cloudformation update-stack \
  --stack-name <nombre-del-stack> \
  --template-body file://<nombre-del-archivo>.yaml \
  --capabilities CAPABILITY_NAMED_IAM
```

### Eliminar un Stack

```bash
aws cloudformation delete-stack --stack-name <nombre-del-stack>
```

---

## 🔍 Validar un Template

Antes de desplegar, se recomienda validar la sintaxis del template:

```bash
aws cloudformation validate-template \
  --template-body file://<nombre-del-archivo>.yaml
```

---

## ⚠️ Consideraciones Importantes

- El template `02-ec2-security-group-elastic-ip.yaml` ahora restringe SSH por parámetro `AdminCidr`; usa tu IP pública con máscara `/32`.
- El flag `--capabilities CAPABILITY_NAMED_IAM` es obligatorio cuando asignas nombres explícitos a recursos IAM, por ejemplo usando `RoleName` en `03-iam-role-vpc-s3-bucket.yaml`.
- El template `01-ec2-basic.yaml` usa por defecto `ami-a4c7edb2`, y permite sobreescribir `AmiId` para otras regiones o AMIs equivalentes.
- `BucketName` en S3 es opcional; si lo defines, debe ser globalmente único en AWS.

---

## 📌 Orden de Aprendizaje Sugerido

```
01-ec2-basic.yaml
       ↓
02-ec2-security-group-elastic-ip.yaml
       ↓
04-iam-user-group-vpc-internet-gateway.yaml
       ↓
05-iam-admin-group-user-vpc-s3.yaml
       ↓
03-iam-role-vpc-s3-bucket.yaml
```

---

## 📚 Referencias

- [Documentación oficial de AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/)
- [Referencia de tipos de recursos](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
- [AWS CLI — CloudFormation](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/)
- [Buenas prácticas de CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)

---

## 👤 Autor

**crisjonhson** — [@crisjonhson](https://github.com/crisjonhson)
