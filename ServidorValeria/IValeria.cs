using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;

using System.Data;          // DataSet

namespace Zuliaworks.Netzuela.Paris.ServidorValeria
{
    [ServiceContract]
    public interface IValeria
    {
        [OperationContract]
        DataSet RecibirTablas();
        [OperationContract]
        void EnviarTablas(string EsquemaXML, string XML);
    }
    /*
    [DataContract]
    public class DataSetXML
    {
        [DataMember]
        public string EsquemaXML { get; set; }
        [DataMember]
        public string XML { get; set; }
    }*/
}
